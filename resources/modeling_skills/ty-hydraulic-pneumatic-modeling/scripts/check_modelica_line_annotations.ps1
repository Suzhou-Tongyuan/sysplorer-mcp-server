param(
    [Parameter(Mandatory = $true)]
    [string]$ModelicaPath,
    [switch]$Json,
    [string]$TargetClass
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'modelica_preflight_common.ps1')

$diagnostics = @()
$connections = @()
$missingLine = @()
$zeroLengthLine = @()
$result = [ordered]@{
    modelica_path = $ModelicaPath
    target_class = $TargetClass
    scope = 'direct connect statements of selected class; nested/inherited classes excluded'
    count_basis = 'syntactic connect statements; loop iterations are not expanded'
    excluded_nested_classes = @()
}
try {
    $scope = Get-MoScope $ModelicaPath $TargetClass
    $result.modelica_path = $scope.Path
    $result.target_class = $scope.Target
    $result.excluded_nested_classes = $scope.ExcludedClasses
    $tokens = $scope.Tokens
    $null = @(Get-MoStatements $tokens)
    for ($i = 0; $i -lt $tokens.Count; $i++) {
        if ($tokens[$i].Kind -ne 'identifier' -or $tokens[$i].Value -cne 'connect') { continue }
        if ($i + 1 -ge $tokens.Count -or $tokens[$i + 1].Value -ne '(') { throw 'malformed_connect_statement' }
        $end = Get-MoClose $tokens ($i + 1)
        $pairTokens = @(Get-MoSlice $tokens ($i + 2) ($end - 1))
        $pair = $pairTokens.Value -join ''
        $hasLine = $false
        $zeroLength = $false
        $after = $end + 1
        if ($after -lt $tokens.Count -and $tokens[$after].Value -ceq 'annotation') {
            if ($after + 1 -ge $tokens.Count -or $tokens[$after + 1].Value -ne '(') { throw 'malformed_connection_annotation' }
            $annotationEnd = Get-MoClose $tokens ($after + 1)
            $fields = Get-MoFields @(Get-MoSlice $tokens ($after + 2) ($annotationEnd - 1))
            if ($fields.ContainsKey('Line')) {
                $line = Get-MoRecord $fields 'Line'
                if ($line.ContainsKey('points')) {
                    $hasLine = $true
                    $points = @(Get-MoNumbers (Get-MoLiteral $line 'points') 'points')
                    $distinct = $false
                    for ($p = 2; $p -lt $points.Count; $p += 2) {
                        if ($points[$p] -ne $points[0] -or $points[$p + 1] -ne $points[1]) { $distinct = $true; break }
                    }
                    $zeroLength = -not $distinct
                }
            }
            $after = $annotationEnd + 1
        }
        if ($after -ge $tokens.Count -or $tokens[$after].Value -ne ';') { throw "unsupported_connect_suffix: $pair" }
        if (-not $hasLine) { $missingLine += $pair }
        if ($zeroLength) { $zeroLengthLine += $pair }
        $connections += [pscustomobject]@{ pair = $pair; has_line_points_annotation = $hasLine; zero_length_line = $zeroLength }
        $i = $after
    }
}
catch { $diagnostics += $_.Exception.Message }

$result['connect_count'] = $connections.Count
$result['line_points_annotation_count'] = @($connections | Where-Object { $_.has_line_points_annotation }).Count
$result['missing_line_annotation_count'] = $missingLine.Count
$result['zero_length_line_count'] = $zeroLengthLine.Count
$result['missing_line_connections'] = $missingLine
$result['zero_length_line_connections'] = $zeroLengthLine
$result['connections'] = $connections
$failed = $missingLine.Count -gt 0 -or $zeroLengthLine.Count -gt 0
Complete-MoPreflight $result $diagnostics $failed -Json:$Json
