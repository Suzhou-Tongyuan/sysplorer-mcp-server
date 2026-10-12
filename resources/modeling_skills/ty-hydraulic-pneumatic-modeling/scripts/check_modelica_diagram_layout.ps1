param(
    [Parameter(Mandatory = $true)]
    [string]$ModelicaPath,
    [double]$MinCenterDistance = 24,
    [switch]$Json,
    [string]$TargetClass
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'modelica_preflight_common.ps1')

$diagnostics = @()
$components = @()
$hidden = @()
$diagramBounds = $null
$result = [ordered]@{
    modelica_path = $ModelicaPath
    target_class = $TargetClass
    scope = 'direct annotations of selected class; nested/inherited classes excluded'
    excluded_nested_classes = @()
}
try {
    if ($MinCenterDistance -lt 0 -or [double]::IsNaN($MinCenterDistance) -or [double]::IsInfinity($MinCenterDistance)) { throw 'invalid_min_center_distance' }
    $scope = Get-MoScope $ModelicaPath $TargetClass
    $result.modelica_path = $scope.Path
    $result.target_class = $scope.Target
    $result.excluded_nested_classes = $scope.ExcludedClasses
    foreach ($annotation in @(Get-MoAnnotations $scope.Tokens)) {
        $fields = $annotation.Fields
        if ($fields.ContainsKey('Diagram')) {
            if ($null -ne $diagramBounds) { throw 'multiple_direct_diagram_annotations' }
            $diagram = Get-MoRecord $fields 'Diagram'
            $coordinates = Get-MoRecord $diagram 'coordinateSystem'
            $bounds = @(Get-MoNumbers (Get-MoLiteral $coordinates 'extent') 'points')
            if ($bounds.Count -ne 4 -or $bounds[0] -ge $bounds[2] -or $bounds[1] -ge $bounds[3]) { throw 'unsupported_diagram_extent' }
            $diagramBounds = [pscustomobject]@{ x1 = $bounds[0]; y1 = $bounds[1]; x2 = $bounds[2]; y2 = $bounds[3] }
        }
        if (-not $fields.ContainsKey('Placement')) { continue }
        $name = Get-MoInstanceName $annotation.Prefix
        $placement = Get-MoRecord $fields 'Placement'
        $visible = Get-MoLiteral $placement 'visible' 'true'
        if ($visible -ceq 'false') { $hidden += $name; continue }
        if ($visible -cne 'true') { throw "unsupported_visibility_expression: $name=$visible" }
        $transform = Get-MoRecord $placement 'transformation'
        $extent = @(Get-MoNumbers (Get-MoLiteral $transform 'extent') 'points')
        $originText = Get-MoLiteral $transform 'origin' '{0,0}'
        $origin = @(Get-MoNumbers "{$originText}" 'points')
        $rotation = @(Get-MoNumbers (Get-MoLiteral $transform 'rotation' '0') 'scalar')
        if ($extent.Count -ne 4 -or $origin.Count -ne 2) { throw "unsupported_transformation_shape: $name" }
        $angle = ($rotation[0] % 360) * [Math]::PI / 180
        $cosine = [Math]::Cos($angle)
        $sine = [Math]::Sin($angle)
        $xs = @()
        $ys = @()
        foreach ($x in @($extent[0], $extent[2])) {
            foreach ($y in @($extent[1], $extent[3])) {
                $xs += $origin[0] + $x * $cosine - $y * $sine
                $ys += $origin[1] + $x * $sine + $y * $cosine
            }
        }
        $minX = ($xs | Measure-Object -Minimum).Minimum
        $maxX = ($xs | Measure-Object -Maximum).Maximum
        $minY = ($ys | Measure-Object -Minimum).Minimum
        $maxY = ($ys | Measure-Object -Maximum).Maximum
        $components += [pscustomobject]@{
            name = $name; rotation = $rotation[0]
            center_x = ($minX + $maxX) / 2; center_y = ($minY + $maxY) / 2
            min_x = $minX; max_x = $maxX; min_y = $minY; max_y = $maxY
        }
    }
}
catch { $diagnostics += $_.Exception.Message }

$epsilon = 1e-9
$outOfBounds = @()
if ($null -ne $diagramBounds) {
    foreach ($c in $components) {
        if ($c.min_x -lt $diagramBounds.x1 - $epsilon -or $c.max_x -gt $diagramBounds.x2 + $epsilon -or $c.min_y -lt $diagramBounds.y1 - $epsilon -or $c.max_y -gt $diagramBounds.y2 + $epsilon) { $outOfBounds += $c.name }
    }
}
$overlaps = @()
$tooClose = @()
$sameCenterCrowding = $false
for ($i = 0; $i -lt $components.Count; $i++) {
    for ($j = $i + 1; $j -lt $components.Count; $j++) {
        $a = $components[$i]
        $b = $components[$j]
        if ($a.min_x -lt $b.max_x - $epsilon -and $a.max_x -gt $b.min_x + $epsilon -and $a.min_y -lt $b.max_y - $epsilon -and $a.max_y -gt $b.min_y + $epsilon) { $overlaps += "$($a.name)<->$($b.name)" }
        $dx = $a.center_x - $b.center_x
        $dy = $a.center_y - $b.center_y
        $distance = [Math]::Sqrt($dx * $dx + $dy * $dy)
        if ($distance -lt $epsilon) { $sameCenterCrowding = $true }
        if ($distance -lt $MinCenterDistance - $epsilon) { $tooClose += "$($a.name)<->$($b.name)" }
    }
}
$result['has_diagram_coordinate_system'] = $null -ne $diagramBounds
$result['diagram_bounds'] = $diagramBounds
$result['placement_count'] = $components.Count
$result['unique_center_count'] = @($components | ForEach-Object { '{0},{1}' -f [Math]::Round($_.center_x, 3), [Math]::Round($_.center_y, 3) } | Select-Object -Unique).Count
$result['placements'] = $components
$result['hidden_instances_not_checked'] = $hidden
$result['same_center_crowding'] = $sameCenterCrowding
$result['out_of_bounds_count'] = $outOfBounds.Count
$result['overlap_count'] = $overlaps.Count
$result['too_close_count'] = $tooClose.Count
$result['out_of_bounds_instances'] = $outOfBounds
$result['overlapping_pairs'] = $overlaps
$result['too_close_pairs'] = $tooClose
$result['geometry_basis'] = 'rotated extent corner bounding boxes; overlap is an axis-aligned-box preflight finding'
$failed = $null -eq $diagramBounds -or $components.Count -eq 0 -or $sameCenterCrowding -or $outOfBounds.Count -gt 0 -or $overlaps.Count -gt 0 -or $tooClose.Count -gt 0
Complete-MoPreflight $result $diagnostics $failed -Json:$Json
