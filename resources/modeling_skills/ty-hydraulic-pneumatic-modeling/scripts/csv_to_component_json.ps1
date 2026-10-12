param(
    [Parameter(Mandatory = $true)]
    [string]$InputPath,

    [string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-HeaderName {
    param(
        [string[]]$Headers,
        [string[]]$Candidates
    )

    foreach ($candidate in $Candidates) {
        $match = $Headers | Where-Object { $_ -eq $candidate } | Select-Object -First 1
        if ($match) {
            return $match
        }
    }

    return $null
}

function Normalize-ComponentType {
    param([string]$Value)

    if (-not $Value) {
        return "unknown"
    }

    $text = $Value.ToLowerInvariant()

    if ($text -match "泵|pump|compressor") { return "pump_or_compressor" }
    if ($text -match "阀|valve") { return "valve" }
    if ($text -match "缸|cylinder|actuator") { return "cylinder" }
    if ($text -match "油箱|tank|reservoir") { return "reservoir" }
    if ($text -match "传感|sensor") { return "sensor" }

    return "unknown"
}

function Split-ParameterText {
    param([string]$Value)

    if (-not $Value) {
        return @()
    }

    return @(
        $Value -split "[,，;；]" |
        ForEach-Object { $_.Trim() } |
        Where-Object { $_ }
    )
}

$resolvedInput = Resolve-Path -LiteralPath $InputPath
$rows = Import-Csv -LiteralPath $resolvedInput

if (-not $rows) {
    throw "No rows found in CSV file: $InputPath"
}

$headers = @($rows[0].PSObject.Properties.Name)
$typeHeader = Resolve-HeaderName -Headers $headers -Candidates @("component_type", "组件类型", "类型", "type", "component")
$qtyHeader = Resolve-HeaderName -Headers $headers -Candidates @("quantity", "数量", "qty", "count")
$paramsHeader = Resolve-HeaderName -Headers $headers -Candidates @("parameters", "主要参数", "参数", "params", "parameter")
$tagHeader = Resolve-HeaderName -Headers $headers -Candidates @("tag", "位号", "标签", "id")
$notesHeader = Resolve-HeaderName -Headers $headers -Candidates @("notes", "备注", "description")

if (-not $typeHeader) {
    throw "Missing required component type column. Expected one of: component_type, 组件类型, 类型, type, component"
}

$normalized = @()
$index = 1

foreach ($row in $rows) {
    $rawType = if ($typeHeader) { [string]$row.$typeHeader } else { "" }
    $rawQty = if ($qtyHeader) { [string]$row.$qtyHeader } else { "1" }
    $rawParams = if ($paramsHeader) { [string]$row.$paramsHeader } else { "" }
    $rawTag = if ($tagHeader) { [string]$row.$tagHeader } else { "" }
    $rawNotes = if ($notesHeader) { [string]$row.$notesHeader } else { "" }

    $quantity = 1
    if ($rawQty -and ($rawQty -as [int])) {
        $quantity = [int]$rawQty
    }

    $normalized += [PSCustomObject]@{
        row_index = $index
        tag = if ($rawTag) { $rawTag } else { "ROW$index" }
        source_component_type = $rawType
        normalized_component_type = Normalize-ComponentType -Value $rawType
        quantity = $quantity
        raw_parameters = $rawParams
        parameter_tokens = @(Split-ParameterText -Value $rawParams)
        notes = $rawNotes
    }

    $index += 1
}

$payload = [PSCustomObject]@{
    input_file = [string]$resolvedInput
    row_count = $normalized.Count
    components = $normalized
}

$json = $payload | ConvertTo-Json -Depth 6

if ($OutputPath) {
    $json | Set-Content -LiteralPath $OutputPath -Encoding UTF8
}
else {
    $json
}
