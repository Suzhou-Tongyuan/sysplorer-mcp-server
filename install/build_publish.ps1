<#
.SYNOPSIS
  Fill publish/sysplorer_mcp: launcher main.py, sysplorer-mcp-server (minus caches/tests), resources, install_mcp.ps1, MCP_BUILD_INFO.json, README.md (from install/windows/README.md).
.NOTES
  Output layout matches Sysplorer Tools/sysplorer_mcp.
  resources/ 为整树复制至 publish 包内；design_opt_mpe_api 等子目录下新增或更新的 Markdown（如 参数估计使用说明.md）无需单独列入复制清单。
  默认发布版：版本号仅为 install/package_version.json 的 version_base（如 0.1）。
  加 -Internal：内部版 version_base.x（x = git rev-list --count HEAD）。
  均写入 publish 内 sysplorer-mcp-server/_build_meta.py 与 MCP_BUILD_INFO.json。
#>
param(
    [string]$RepoRoot = "",
    [switch]$Internal
)

$ErrorActionPreference = "Stop"

function Get-LegacyChineseManualFileName {
    # UTF-8 bytes for: 安装部署手册.md (cleanup only; ASCII-safe in PS 5.1)
    [System.Text.Encoding]::UTF8.GetString([byte[]]@(
        0xE5, 0xAE, 0x89, 0xE8, 0xA3, 0x85, 0xE9, 0x83, 0xA8, 0xE7, 0xBD, 0xB2, 0xE6, 0x89, 0x8B, 0xE5, 0x86, 0x8C, 0x2E, 0x6D, 0x64
    ))
}

if (-not $RepoRoot) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}

$InstallDir = $PSScriptRoot
$PublishRoot = Join-Path $RepoRoot "publish\sysplorer_mcp"
$LauncherSrc = Join-Path $InstallDir "publish_assets\sysplorer_mcp_main.py"
$ServerSrc = Join-Path $RepoRoot "sysplorer-mcp-server"
$ResSrc = Join-Path $RepoRoot "resources"
$InstallScriptSrc = Join-Path $RepoRoot "install_sysplorer_mcp_tools.ps1"
$InstallScriptShSrc = Join-Path $RepoRoot "install_mcp.sh"
$ReadmeSrc = Join-Path $InstallDir "windows\README.md"
$WriteMeta = Join-Path $InstallDir "write_build_meta.py"
$PkgVerJson = Join-Path $InstallDir "package_version.json"

if (-not (Test-Path -LiteralPath $LauncherSrc)) {
    throw "Missing launcher source: $LauncherSrc"
}
if (-not (Test-Path -LiteralPath $ServerSrc)) {
    throw "Missing sysplorer-mcp-server: $ServerSrc"
}
if (-not (Test-Path -LiteralPath $ResSrc)) {
    throw "Missing resources: $ResSrc"
}
if (-not (Test-Path -LiteralPath $InstallScriptSrc)) {
    throw "Missing install_sysplorer_mcp_tools.ps1 at repo root"
}
if (-not (Test-Path -LiteralPath $InstallScriptShSrc)) {
    throw "Missing install_mcp.sh: $InstallScriptShSrc"
}
if (-not (Test-Path -LiteralPath $ReadmeSrc)) {
    throw "Missing install/windows/README.md (copied into release bundle as README.md): $ReadmeSrc"
}
if (-not (Test-Path -LiteralPath $WriteMeta)) {
    throw "Missing write_build_meta.py: $WriteMeta"
}
if (-not (Test-Path -LiteralPath $PkgVerJson)) {
    throw "Missing package_version.json: $PkgVerJson"
}

$metaMode = if ($Internal) { "internal" } else { "release" }

Write-Host "Repo:    $RepoRoot" -ForegroundColor Cyan
Write-Host "Publish: $PublishRoot" -ForegroundColor Cyan
Write-Host "Mode:    $metaMode" -ForegroundColor Cyan

New-Item -ItemType Directory -Path $PublishRoot -Force | Out-Null

Copy-Item -LiteralPath $LauncherSrc -Destination (Join-Path $PublishRoot "main.py") -Force

$ServerDst = Join-Path $PublishRoot "sysplorer-mcp-server"
if (Test-Path -LiteralPath $ServerDst) {
    Remove-Item -LiteralPath $ServerDst -Recurse -Force
}
New-Item -ItemType Directory -Path $ServerDst -Force | Out-Null
$robolog = Join-Path $env:TEMP ("robocopy_publish_" + [Guid]::NewGuid().ToString("n") + ".log")
$null = & robocopy $ServerSrc $ServerDst /E /XD __pycache__ tests .pytest_cache /XF *.pyc /XF modelica_doc_index.json /NFL /NDL /NJH /NJS /nc /ns /np /LOG:$robolog
$rc = $LASTEXITCODE
if ($rc -ge 8) {
    throw "robocopy sysplorer-mcp-server failed (exit $rc). See $robolog"
}

$ResDst = Join-Path $PublishRoot "resources"
if (Test-Path -LiteralPath $ResDst) {
    Remove-Item -LiteralPath $ResDst -Recurse -Force
}
$resSrcFull = (Resolve-Path -LiteralPath $ResSrc).Path
Copy-Item -LiteralPath $resSrcFull -Destination $ResDst -Recurse -Force
$ragHuge = "modelica_doc_index.json"
Get-ChildItem -LiteralPath $ResDst -Recurse -Force -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -eq $ragHuge } |
    ForEach-Object {
        Write-Host "Omitting large RAG index from publish: $($_.Name)" -ForegroundColor DarkYellow
        Remove-Item -LiteralPath $_.FullName -Force -ErrorAction Stop
    }
$nResSrc = @(Get-ChildItem -LiteralPath $ResSrc -Recurse -Force -File -ErrorAction Stop | Where-Object { $_.Name -ne $ragHuge }).Count
$nResDst = @(Get-ChildItem -LiteralPath $ResDst -Recurse -Force -File -ErrorAction Stop | Where-Object { $_.Name -ne $ragHuge }).Count
if ($nResSrc -ne $nResDst) {
    throw "resources file count mismatch: src=$nResSrc dst=$nResDst"
}

Copy-Item -LiteralPath $InstallScriptSrc -Destination (Join-Path $PublishRoot "install_mcp.ps1") -Force
Copy-Item -LiteralPath $InstallScriptShSrc -Destination (Join-Path $PublishRoot "install_mcp.sh") -Force

$distInstallPs1 = Join-Path $PublishRoot "install_mcp.ps1"
$ps1Text = [System.IO.File]::ReadAllText($distInstallPs1, [System.Text.UTF8Encoding]::new($false))
if ($ps1Text.Length -gt 0 -and [int][char]$ps1Text[0] -eq 0xFEFF) { $ps1Text = $ps1Text.Substring(1) }
$utf8Bom = New-Object System.Text.UTF8Encoding($true)
[System.IO.File]::WriteAllText($distInstallPs1, $ps1Text, $utf8Bom)

$metaDst = Join-Path $ServerDst "_build_meta.py"
$buildInfoJson = $null
$metaOk = $false
if (Get-Command py -ErrorAction SilentlyContinue) {
    $buildInfoJson = & py -3 $WriteMeta --repo-root $RepoRoot --mode $metaMode --output $metaDst --print-json 2>$null
    if ($LASTEXITCODE -eq 0) { $metaOk = $true }
}
if (-not $metaOk) {
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        throw "write_build_meta.py requires py -3 or python on PATH"
    }
    $buildInfoJson = & python $WriteMeta --repo-root $RepoRoot --mode $metaMode --output $metaDst --print-json 2>$null
    if ($LASTEXITCODE -ne 0) { throw "write_build_meta.py failed (exit $LASTEXITCODE)" }
}
$buildInfo = $buildInfoJson | ConvertFrom-Json
$versionDisplayPub = [string]$buildInfo.version_display
if ([string]::IsNullOrWhiteSpace($versionDisplayPub)) { $versionDisplayPub = [string]$buildInfo.version }
Write-Host "Version: $versionDisplayPub" -ForegroundColor Green
$BuildInfoPath = Join-Path $PublishRoot "MCP_BUILD_INFO.json"
$buildInfoObj = [ordered]@{
    version            = [string]$buildInfo.version
    version_display    = $versionDisplayPub
    version_base       = [string]$buildInfo.version_base
    version_core       = [string]$buildInfo.version_core
    build_counter      = [int]$buildInfo.build_counter
    git_commit_count   = [int]$buildInfo.git_commit_count
    build_kind         = [string]$buildInfo.build_kind
    build_time         = [string]$buildInfo.build_time
    git_revision       = [string]$buildInfo.git_revision
}
($buildInfoObj | ConvertTo-Json -Depth 5) | Set-Content -Path $BuildInfoPath -Encoding UTF8
Write-Host "Wrote $BuildInfoPath" -ForegroundColor DarkGray

$readmeDst = Join-Path $PublishRoot "README.md"
$legacyReadmeTxt = Join-Path $PublishRoot "README.txt"
$legacyReadmeMd = Join-Path $PublishRoot "Readme.md"
$legacyInstallManualEn = Join-Path $PublishRoot "INSTALL_MANUAL.md"
$legacyChineseManual = Join-Path $PublishRoot (Get-LegacyChineseManualFileName)
foreach ($p in @($legacyReadmeTxt, $legacyReadmeMd, $legacyInstallManualEn, $legacyChineseManual)) {
    if (Test-Path -LiteralPath $p) {
        Remove-Item -LiteralPath $p -Force
    }
}
Copy-Item -LiteralPath $ReadmeSrc -Destination $readmeDst -Force
Write-Host "Wrote README: $readmeDst" -ForegroundColor DarkGray

Write-Host "Done. Output: $PublishRoot  ($versionDisplayPub)" -ForegroundColor Green
