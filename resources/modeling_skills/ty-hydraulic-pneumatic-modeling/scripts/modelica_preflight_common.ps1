# Shared, deliberately bounded lexical preflight. No Modelica code is evaluated.
# Unsupported/ambiguous syntax is reported as undetermined by the callers.

function Get-MoTokens {
    param([string]$Text)
    $pattern = @'
\G(?:(?<space>\s+)|(?<line>//[^\r\n]*)|(?<block>/\*[\s\S]*?\*/)|(?<string>"(?:\\[\s\S]|[^"\\])*")|(?<quoted>'(?:\\[\s\S]|[^'\\])*')|(?<number>(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)|(?<identifier>[A-Za-z_][A-Za-z_0-9]*)|(?<symbol>[\s\S]))
'@
    $regex = [regex]::new($pattern.Trim())
    $items = [System.Collections.Generic.List[object]]::new()
    $offset = 0
    while ($offset -lt $Text.Length) {
        $match = $regex.Match($Text, $offset)
        if (-not $match.Success -or $match.Index -ne $offset) { throw "unsupported_lexeme: offset $offset" }
        if ($match.Groups['symbol'].Success -and ($match.Value -eq '"' -or $match.Value -eq "'" -or ($match.Value -eq '/' -and $Text.Substring($offset).StartsWith('/*')))) {
            throw "unterminated_string_or_comment: offset $offset"
        }
        if (-not ($match.Groups['space'].Success -or $match.Groups['line'].Success -or $match.Groups['block'].Success)) {
            $kind = 'symbol'
            foreach ($candidate in @('string', 'quoted', 'number', 'identifier')) {
                if ($match.Groups[$candidate].Success) { $kind = $candidate; break }
            }
            $items.Add([pscustomobject]@{ Value = $match.Value; Kind = $kind; Offset = $offset })
        }
        $offset += $match.Length
    }
    return [pscustomobject]@{ Tokens = @($items.ToArray()) }
}

function Get-MoClose {
    param([object[]]$Tokens, [int]$Start)
    $pairs = @{ '(' = ')'; '{' = '}'; '[' = ']' }
    $stack = [System.Collections.Generic.List[string]]::new()
    if (-not $pairs.ContainsKey($Tokens[$Start].Value)) { throw 'expected_open_delimiter' }
    for ($i = $Start; $i -lt $Tokens.Count; $i++) {
        $token = $Tokens[$i]
        if ($token.Kind -ne 'symbol') { continue }
        if ($pairs.ContainsKey($token.Value)) { $stack.Add($pairs[$token.Value]) }
        elseif ($token.Value -in @(')', '}', ']')) {
            if ($stack.Count -eq 0 -or $token.Value -ne $stack[$stack.Count - 1]) { throw 'unbalanced_delimiters' }
            $stack.RemoveAt($stack.Count - 1)
            if ($stack.Count -eq 0) { return $i }
        }
    }
    throw 'unclosed_delimiter'
}

function Get-MoSlice {
    param([object[]]$Tokens, [int]$Start, [int]$End)
    if ($End -lt $Start) { return }
    for ($i = $Start; $i -le $End; $i++) { $Tokens[$i] }
}

function Get-MoScope {
    param([string]$Path, [string]$TargetClass)
    $resolved = (Resolve-Path -LiteralPath $Path).Path
    $text = [System.IO.File]::ReadAllText($resolved, [System.Text.UTF8Encoding]::new($false, $true))
    $tokens = (Get-MoTokens $text).Tokens
    $classes = [System.Collections.Generic.List[object]]::new()
    $shortClasses = [System.Collections.Generic.List[object]]::new()
    $stack = [System.Collections.Generic.List[int]]::new()
    $within = ''
    if ($tokens.Count -gt 0 -and $tokens[0].Value -ceq 'within') {
        $i = 1
        while ($i -lt $tokens.Count -and $tokens[$i].Value -ne ';') {
            if ($tokens[$i].Kind -ne 'identifier' -and $tokens[$i].Value -ne '.') { throw 'unsupported_within_clause' }
            $within += $tokens[$i].Value
            $i++
        }
        if ($i -eq $tokens.Count) { throw 'unclosed_within_clause' }
    }
    $classKinds = @('model', 'block', 'package', 'connector', 'record', 'function', 'type', 'class', 'operator')
    for ($i = 0; $i -lt $tokens.Count; $i++) {
        $token = $tokens[$i]
        # Class declarations cannot start inside a modifier, annotation or array subscript.
        if ($token.Kind -eq 'symbol' -and $token.Value -in @('(', '{', '[')) { $i = Get-MoClose $tokens $i; continue }
        if ($token.Kind -ne 'identifier') { continue }
        if ($token.Value -ceq 'end' -and $i + 2 -lt $tokens.Count -and $tokens[$i + 2].Value -eq ';') {
            $name = $tokens[$i + 1].Value
            if ($name -cin @('if', 'for', 'when', 'while', 'match', 'try')) { $i += 2; continue }
            if ($stack.Count -eq 0) { throw "unexpected_class_end: $name" }
            $current = $classes[$stack[$stack.Count - 1]]
            if ($current.Name -cne $name) { throw "mismatched_class_end: expected $($current.Name), got $name" }
            $current.End = $i + 2
            $current.BodyEnd = $i - 1
            $stack.RemoveAt($stack.Count - 1)
            $i += 2
            continue
        }
        if ($token.Value -cnotin $classKinds) { continue }
        # operator record/function is a prefix, whereas operator Name is a class.
        if ($token.Value -ceq 'operator' -and $i + 1 -lt $tokens.Count -and $tokens[$i + 1].Value -cin @('record', 'function')) { continue }
        $nameIndex = $i + 1
        if ($nameIndex -lt $tokens.Count -and $tokens[$nameIndex].Value -ceq 'extends') { $nameIndex++ }
        if ($nameIndex -ge $tokens.Count -or $tokens[$nameIndex].Kind -ne 'identifier') { throw 'unsupported_class_name' }
        $name = $tokens[$nameIndex].Value
        $afterName = $nameIndex + 1
        $parent = if ($stack.Count -gt 0) { $stack[$stack.Count - 1] } else { -1 }
        $prefix = if ($parent -ge 0) { $classes[$parent].FullName } else { $within }
        $fullName = if ($prefix) { "$prefix.$name" } else { $name }
        if ($afterName -lt $tokens.Count -and $tokens[$afterName].Value -eq '=') {
            # A short class has no independent graphical body. Skip its balanced definition.
            $shortStart = $i
            $i = $afterName + 1
            while ($i -lt $tokens.Count -and $tokens[$i].Value -ne ';') {
                if ($tokens[$i].Value -in @('(', '{', '[')) { $i = Get-MoClose $tokens $i }
                $i++
            }
            if ($i -ge $tokens.Count) { throw "unclosed_short_class: $name" }
            $shortClasses.Add([pscustomobject]@{ Start = $shortStart; End = $i; FullName = $fullName })
            continue
        }
        $classes.Add([pscustomobject]@{ Name = $name; FullName = $fullName; Parent = $parent; Start = $i; BodyStart = $afterName; BodyEnd = -1; End = -1 })
        $stack.Add($classes.Count - 1)
        $i = $nameIndex
    }
    if ($stack.Count -gt 0) { throw 'unclosed_class' }
    if ($classes.Count -eq 0) { throw 'no_long_class: short classes/inherited graphics require separate evidence' }
    if ($TargetClass) {
        $selected = @($classes | Where-Object { $_.FullName -ceq $TargetClass })
        if ($selected.Count -eq 0) { $selected = @($classes | Where-Object { $_.Name -ceq $TargetClass }) }
        if ($selected.Count -ne 1) { throw "target_class_missing_or_ambiguous: $TargetClass; available=$($classes.FullName -join ',')" }
    }
    else {
        if ($classes.Count -ne 1) { throw "target_class_required: available=$($classes.FullName -join ',')" }
        $selected = @($classes[0])
    }
    $target = $selected[0]
    $direct = [System.Collections.Generic.List[object]]::new()
    $children = @(@($classes.ToArray()) + @($shortClasses.ToArray()) | Where-Object { $_.Start -gt $target.Start -and $_.End -lt $target.End })
    for ($i = $target.BodyStart; $i -le $target.BodyEnd; $i++) {
        $child = @($children | Where-Object { $_.Start -eq $i })
        if ($child.Count -gt 0) {
            $i = $child[0].End
            # Preserve a boundary so a child declaration cannot merge surrounding statements.
            $direct.Add([pscustomobject]@{ Value = ';'; Kind = 'symbol'; Offset = -1 })
        }
        else { $direct.Add($tokens[$i]) }
    }
    return [pscustomobject]@{ Path = $resolved; Target = $target.FullName; Tokens = @($direct.ToArray()); ExcludedClasses = @($children | ForEach-Object { $_.FullName }) }
}

function Get-MoStatements {
    param([object[]]$Tokens)
    $start = 0
    for ($i = 0; $i -lt $Tokens.Count; $i++) {
        if ($Tokens[$i].Kind -eq 'symbol' -and $Tokens[$i].Value -in @('(', '{', '[')) { $i = Get-MoClose $Tokens $i }
        elseif ($Tokens[$i].Kind -eq 'symbol' -and $Tokens[$i].Value -eq ';') {
            if ($i -gt $start) { [pscustomobject]@{ Tokens = @(Get-MoSlice $Tokens $start ($i - 1)) } }
            $start = $i + 1
        }
    }
    if ($start -lt $Tokens.Count) { throw 'unterminated_statement' }
}

function Get-MoFields {
    param([object[]]$Tokens)
    $fields = [System.Collections.Generic.Dictionary[string, object]]::new([System.StringComparer]::Ordinal)
    $start = 0
    for ($i = 0; $i -le $Tokens.Count; $i++) {
        if ($i -lt $Tokens.Count -and $Tokens[$i].Value -in @('(', '{', '[')) { $i = Get-MoClose $Tokens $i; continue }
        if ($i -eq $Tokens.Count -or $Tokens[$i].Value -eq ',') {
            $part = @(Get-MoSlice $Tokens $start ($i - 1))
            if ($part.Count -gt 0) {
                if ($part.Count -lt 2 -or $part[0].Kind -ne 'identifier' -or $part[1].Value -notin @('=', '(')) { throw 'unsupported_annotation_argument' }
                $name = $part[0].Value
                if ($fields.ContainsKey($name)) { throw "duplicate_annotation_argument: $name" }
                if ($part[1].Value -eq '(') {
                    if ((Get-MoClose $part 1) -ne $part.Count - 1) { throw "unsupported_annotation_record: $name" }
                    $fields.Add($name, [pscustomobject]@{ Form = 'record'; Tokens = @(Get-MoSlice $part 2 ($part.Count - 2)) })
                }
                else { $fields.Add($name, [pscustomobject]@{ Form = 'value'; Tokens = @(Get-MoSlice $part 2 ($part.Count - 1)) }) }
            }
            $start = $i + 1
        }
    }
    return ,$fields
}

function Get-MoRecord {
    param($Fields, [string]$Name)
    if (-not $Fields.ContainsKey($Name) -or $Fields[$Name].Form -ne 'record') { throw "missing_or_unsupported_record: $Name" }
    return ,(Get-MoFields $Fields[$Name].Tokens)
}

function Get-MoLiteral {
    param($Fields, [string]$Name, [string]$Default)
    if (-not $Fields.ContainsKey($Name)) {
        if ($Default) { return $Default }
        throw "missing_literal: $Name"
    }
    if ($Fields[$Name].Form -ne 'value') { throw "unsupported_literal: $Name" }
    return ($Fields[$Name].Tokens.Value -join '')
}

function Get-MoNumbers {
    param([string]$Text, [ValidateSet('scalar', 'points')][string]$Shape)
    $number = '[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?'
    $valid = if ($Shape -eq 'scalar') { "^(?:$number)$" } else { "^\{\{$number,$number\}(?:,\{$number,$number\})*\}$" }
    if ($Text -cnotmatch $valid) { throw "unsupported_numeric_expression: $Text" }
    foreach ($match in [regex]::Matches($Text, $number)) {
        $value = [double]::Parse($match.Value, [System.Globalization.CultureInfo]::InvariantCulture)
        if ([double]::IsNaN($value) -or [double]::IsInfinity($value)) { throw 'non_finite_coordinate' }
        $value
    }
}

function Get-MoAnnotations {
    param([object[]]$Tokens)
    foreach ($statement in @(Get-MoStatements $Tokens)) {
        $part = $statement.Tokens
        for ($i = 0; $i -lt $part.Count; $i++) {
            if ($part[$i].Kind -eq 'identifier' -and $part[$i].Value -ceq 'annotation') {
                if ($i + 1 -ge $part.Count -or $part[$i + 1].Value -ne '(') { throw 'malformed_annotation' }
                $end = Get-MoClose $part ($i + 1)
                [pscustomobject]@{ Prefix = @(Get-MoSlice $part 0 ($i - 1)); Fields = (Get-MoFields @(Get-MoSlice $part ($i + 2) ($end - 1))) }
                $i = $end
            }
            elseif ($part[$i].Kind -eq 'symbol' -and $part[$i].Value -in @('(', '{', '[')) { $i = Get-MoClose $part $i }
        }
    }
}

function Get-MoInstanceName {
    param([object[]]$Prefix)
    $i = 0
    while ($i -lt $Prefix.Count -and ($Prefix[$i].Kind -eq 'string' -or $Prefix[$i].Value -cin @('public', 'protected', 'inner', 'outer', 'input', 'output', 'flow', 'stream', 'discrete', 'parameter', 'constant', 'final', 'replaceable', 'redeclare', 'each'))) { $i++ }
    if ($i -ge $Prefix.Count -or $Prefix[$i].Kind -ne 'identifier') { throw 'unsupported_component_declaration' }
    $i++
    while ($i + 1 -lt $Prefix.Count -and $Prefix[$i].Value -eq '.' -and $Prefix[$i + 1].Kind -eq 'identifier') { $i += 2 }
    if ($i -ge $Prefix.Count -or $Prefix[$i].Kind -ne 'identifier') { throw 'unsupported_component_name_or_array' }
    $name = $Prefix[$i].Value
    $i++
    for (; $i -lt $Prefix.Count; $i++) {
        if ($Prefix[$i].Value -eq '(') { $i = Get-MoClose $Prefix $i }
        elseif ($Prefix[$i].Value -in @('[', ',', 'if')) { throw "unsupported_array_multiple_or_conditional_component: $name" }
    }
    return $name
}

function Complete-MoPreflight {
    param([System.Collections.IDictionary]$Result, [object[]]$Diagnostics, [bool]$KnownFailure, [switch]$Json)
    $status = if ($Diagnostics.Count -gt 0) { 'undetermined' } elseif ($KnownFailure) { 'failed' } else { 'passed' }
    $Result['status'] = $status
    $Result['passed'] = if ($status -eq 'undetermined') { $null } else { $status -eq 'passed' }
    $Result['diagnostics'] = @($Diagnostics)
    if ($Json) { [pscustomobject]$Result | ConvertTo-Json -Depth 10 }
    else { [pscustomobject]$Result | Format-List }
    if ($status -eq 'undetermined') { exit 2 }
    if ($status -eq 'failed') { exit 1 }
    exit 0
}
