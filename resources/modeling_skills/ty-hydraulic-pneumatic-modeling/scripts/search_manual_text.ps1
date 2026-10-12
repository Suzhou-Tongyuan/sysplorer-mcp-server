param(
    [Parameter(Mandatory = $true)]
    [string[]]$Keyword,

    [string]$LibraryName,

    [int]$First = 40
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$dir = Join-Path (Split-Path -Parent $PSScriptRoot) 'references\manual-text'
$files = Get-ChildItem -LiteralPath $dir -Filter '*.md'

if ($LibraryName) {
    $files = $files | Where-Object { $_.BaseName -like "*$LibraryName*" }
}

$results = foreach ($file in $files) {
    foreach ($term in $Keyword) {
        Select-String -Path $file.FullName -Pattern $term -SimpleMatch | ForEach-Object {
            [PSCustomObject]@{
                文件 = $file.BaseName
                行号 = $_.LineNumber
                关键词 = $term
                内容 = $_.Line.Trim()
            }
        }
    }
}

$results | Select-Object -First $First | Format-Table -Wrap -AutoSize


