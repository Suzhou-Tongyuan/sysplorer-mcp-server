<#
.SYNOPSIS
  使用指定 Python 3.12 构建 PyInstaller exe，并填充 publish/sysplorer_mcp_exe（exe + resources + 安装脚本 + MCP_BUILD_INFO.json + README）。
.NOTES
  - 默认 Python：D:\Python312\python.exe（可用 -PythonExe 覆盖）。
  - 默认输出：仓库 publish/sysplorer_mcp_exe/（与 build_publish.ps1 的 publish/sysplorer_mcp 并列）。
  - mworks.sysplorer 需可 import：设置 MWORKS_INSTALL_DIR，或 -MworksInstallDir，或脚本会从 E:\SysplorerSoftware 下自动探测。
  - 版本：默认发布版（version_base）；加 -Internal 为内部版 version_base.<git commit count>。
  - resources/ 同步规则与 build_publish.ps1 一致（省略 modelica_doc_index.json、/XD generated）。
#>
param(
    [string]$RepoRoot = "",
    [string]$PythonExe = "D:\Python312\python.exe",
    [string]$MworksInstallDir = $env:MWORKS_INSTALL_DIR,
    [switch]$Internal
)

$ErrorActionPreference = "Stop"

$script:RoboQuiet = @("/NFL", "/NDL", "/NJH", "/NJS", "/nc", "/ns", "/np")
$script:RoboRetry = @("/R:2", "/W:1")

function Assert-RobocopyExitCode {
    param([int]$Rc, [string]$What)
    if ($Rc -ge 8) {
        throw "robocopy $What failed (exit $Rc)"
    }
}

function Remove-TreeBestEffort {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return }
    try {
        Remove-Item -LiteralPath $Path -Recurse -Force -ErrorAction Stop
    } catch {
        throw "Cannot remove: $Path — $($_.Exception.Message)"
    }
}

function Write-RobocopyLogTail {
    param([string]$LogPath, [int]$Lines = 35)
    if (-not $LogPath -or -not (Test-Path -LiteralPath $LogPath)) { return }
    Write-Host "--- robocopy log tail: $LogPath ---" -ForegroundColor Yellow
    Get-Content -LiteralPath $LogPath -Tail $Lines -ErrorAction SilentlyContinue | ForEach-Object { Write-Host $_ }
    Write-Host "--- end log tail ---" -ForegroundColor Yellow
}

function Copy-ResourceFileByteFallback {
    param([string]$SourceFile, [string]$DestFile)
    if (-not (Test-Path -LiteralPath $SourceFile)) { return }
    $dir = Split-Path -Parent $DestFile
    if (-not (Test-Path -LiteralPath $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    $bytes = [System.IO.File]::ReadAllBytes($SourceFile)
    [System.IO.File]::WriteAllBytes($DestFile, $bytes)
}

function Repair-MissingResourceFilesAfterRobocopy {
    param(
        [string]$SourceRoot,
        [string]$DestRoot,
        [string]$ExcludeFileName,
        [scriptblock]$SkipPath
    )
    $srcRoot = (Resolve-Path -LiteralPath $SourceRoot).Path
    $n = 0
    Get-ChildItem -LiteralPath $srcRoot -Recurse -Force -File -ErrorAction Stop | Where-Object {
        $_.Name -ne $ExcludeFileName -and -not (& $SkipPath $_.FullName)
    } | ForEach-Object {
        $rel = $_.FullName.Substring($srcRoot.Length).TrimStart('\')
        $destFile = Join-Path $DestRoot $rel
        $need = $false
        if (-not (Test-Path -LiteralPath $destFile)) {
            $need = $true
        } else {
            $dl = (Get-Item -LiteralPath $destFile).Length
            if ($dl -ne $_.Length) { $need = $true }
        }
        if ($need) {
            Write-Host "  byte-fallback: $rel" -ForegroundColor DarkYellow
            Copy-ResourceFileByteFallback -SourceFile $_.FullName -DestFile $destFile
            $n++
        }
    }
    if ($n -gt 0) {
        Write-Host "  byte-fallback applied to $n file(s)" -ForegroundColor DarkGray
    }
}

function Invoke-QuietPip {
    param([string]$PythonExePath, [string[]]$Args)
    $old = $ErrorActionPreference
    $ErrorActionPreference = "SilentlyContinue"
    try {
        & $PythonExePath -X utf8 -m pip @Args 1>$null 2>$null
    } finally {
        $ErrorActionPreference = $old
    }
}

function Copy-MworksSitePackages {
    param(
        [Parameter(Mandatory = $true)][string]$MworksRoot,
        [Parameter(Mandatory = $true)][string]$VenvSitePackages
    )
    $src = Join-Path $MworksRoot "External\python64\Lib\site-packages"
    if (-not (Test-Path $src)) {
        throw "Sysplorer site-packages not found: $src"
    }
    Write-Host "Copying mworks* / sysplorer* from: $src" -ForegroundColor Cyan
    Get-ChildItem -Path $src -ErrorAction SilentlyContinue | ForEach-Object {
        $n = $_.Name
        if ($n -like "mworks*" -or $n -like "sysplorer*" -or $n -like "jsonrpc*" -or $n -like "psutil*") {
            $dest = Join-Path $VenvSitePackages $n
            if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
            Copy-Item -Path $_.FullName -Destination $dest -Recurse -Force
        }
    }
}

function Test-PyImport {
    param([string]$PythonExePath, [string]$Code)
    $prev = $ErrorActionPreference
    $ErrorActionPreference = "SilentlyContinue"
    try {
        $out = & $PythonExePath -c $Code 2>$null
        return ($out -match "ok")
    } finally {
        $ErrorActionPreference = $prev
    }
}

function Resolve-MworksInstallDir {
    param([string]$Explicit)
    if (-not [string]::IsNullOrWhiteSpace($Explicit) -and (Test-Path -LiteralPath $Explicit)) {
        return (Resolve-Path -LiteralPath $Explicit).Path
    }
    $root = "E:\SysplorerSoftware"
    if (-not (Test-Path -LiteralPath $root)) { return $null }
    $candidates = @(Get-ChildItem -LiteralPath $root -Directory -ErrorAction SilentlyContinue | Where-Object {
            Test-Path (Join-Path $_.FullName "External\python64\Lib\site-packages\mworks")
        })
    if ($candidates.Count -eq 0) { return $null }
    return ($candidates | Sort-Object Name -Descending | Select-Object -First 1).FullName
}

if (-not $RepoRoot) {
    if (Test-Path -LiteralPath (Join-Path $PSScriptRoot "install")) {
        $RepoRoot = (Resolve-Path $PSScriptRoot).Path
    } else {
        $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
    }
} else {
    $RepoRoot = (Resolve-Path $RepoRoot).Path
}

$InstallDir = Join-Path $RepoRoot "install"
$PublishRoot = Join-Path $RepoRoot "publish\sysplorer_mcp_exe"
$BuildDir = Join-Path $InstallDir "build-exe-publish"
$HelperBuildDir = Join-Path $InstallDir "build-helper-publish"
$SpecFile = Join-Path $InstallDir "windows\sysplorer_mcp_server.spec"
$HelperSrc = Join-Path $InstallDir "helpers\install_library_helper.py"
$WriteMeta = Join-Path $InstallDir "write_build_meta.py"
$PkgVerJson = Join-Path $InstallDir "package_version.json"
$ResSrc = Join-Path $RepoRoot "resources"
$ReadmeSrc = Join-Path $InstallDir "windows\README.md"
$InstallScriptSrc = Join-Path $InstallDir "windows\install_mcp_exe.ps1"
$InstallScriptShSrc = Join-Path $RepoRoot "install_mcp.sh"
$InstallMcpSilentSrc = Join-Path $InstallDir "install_mcp_silent.py"
$MetaDst = Join-Path $RepoRoot "sysplorer-mcp-server\_build_meta.py"

if (-not (Test-Path -LiteralPath $PythonExe)) {
    throw "Python not found: $PythonExe"
}
if (-not (Test-Path -LiteralPath $SpecFile)) { throw "Missing $SpecFile" }
if (-not (Test-Path -LiteralPath $HelperSrc)) { throw "Missing $HelperSrc" }
if (-not (Test-Path -LiteralPath $WriteMeta)) { throw "Missing $WriteMeta" }
if (-not (Test-Path -LiteralPath $PkgVerJson)) { throw "Missing $PkgVerJson" }
if (-not (Test-Path -LiteralPath $ResSrc)) { throw "Missing resources: $ResSrc" }
if (-not (Test-Path -LiteralPath $ReadmeSrc)) { throw "Missing $ReadmeSrc" }
if (-not (Test-Path -LiteralPath $InstallScriptSrc)) { throw "Missing $InstallScriptSrc" }

$mworksDir = Resolve-MworksInstallDir -Explicit $MworksInstallDir
$metaMode = if ($Internal) { "internal" } else { "release" }

Write-Host "Repo:     $RepoRoot" -ForegroundColor Cyan
Write-Host "Publish:  $PublishRoot" -ForegroundColor Cyan
Write-Host "Python:   $PythonExe" -ForegroundColor Cyan
Write-Host "Mode:     $metaMode" -ForegroundColor Cyan
if ($mworksDir) {
    Write-Host "Sysplorer: $mworksDir" -ForegroundColor Cyan
} else {
    Write-Warning "MWORKS_INSTALL_DIR not set and auto-detect failed; mworks.sysplorer import may fail."
}

# --- prepare publish root ---
Write-Host "Prepare publish folder..." -ForegroundColor DarkGray
New-Item -ItemType Directory -Path $PublishRoot -Force | Out-Null
Get-ChildItem -LiteralPath $PublishRoot -Force -ErrorAction SilentlyContinue | ForEach-Object {
    Remove-TreeBestEffort -Path $_.FullName
}

# --- use the provided Python environment directly ---
$Py = (Resolve-Path -LiteralPath $PythonExe).Path
if ($mworksDir) {
    $env:MWORKS_INSTALL_DIR = $mworksDir
}
Write-Host "Use Python directly; no venv/pip install." -ForegroundColor DarkGray
if (-not (Test-PyImport -PythonExePath $Py -Code "import PyInstaller; print('ok')")) {
    throw "Prerequisite missing in Python environment: PyInstaller"
}
if (-not (Test-PyImport -PythonExePath $Py -Code "import mcp, zstandard, mworks.sysplorer, win32api, jsonrpcclient, websocket, psutil; print('ok')")) {
    throw "Prerequisite missing in Python environment. Required imports: mcp, zstandard, mworks.sysplorer, win32api, jsonrpcclient, websocket, psutil"
}

# --- build metadata (embedded into exe via PyInstaller) ---
Write-Host "Write build metadata..." -ForegroundColor DarkGray
$buildInfoJson = & $Py $WriteMeta --repo-root $RepoRoot --mode $metaMode --output $MetaDst --print-json
if ($LASTEXITCODE -ne 0) { throw "write_build_meta.py failed (exit $LASTEXITCODE)" }
$buildInfo = $buildInfoJson | ConvertFrom-Json
$versionDisplayPub = [string]$buildInfo.version_display
if ([string]::IsNullOrWhiteSpace($versionDisplayPub)) { $versionDisplayPub = [string]$buildInfo.version }
Write-Host "Version: $versionDisplayPub" -ForegroundColor Green

# --- PyInstaller ---
New-Item -ItemType Directory -Path $BuildDir -Force | Out-Null

Write-Host "PyInstaller -> $PublishRoot ..." -ForegroundColor Cyan
Push-Location $InstallDir
try {
    & $Py -m PyInstaller --noconfirm --clean `
        --distpath $PublishRoot `
        --workpath $BuildDir `
        $SpecFile
    if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed (exit $LASTEXITCODE)" }
} finally {
    Pop-Location
}

$Exe = Join-Path $PublishRoot "sysplorer_mcp_server.exe"
if (-not (Test-Path -LiteralPath $Exe)) {
    throw "Build failed: $Exe not found"
}

# --- elevated install helper ---
$HelperExe = Join-Path $PublishRoot "install-helper.exe"
New-Item -ItemType Directory -Path $HelperBuildDir -Force | Out-Null
Write-Host "PyInstaller helper -> $HelperExe ..." -ForegroundColor Cyan
Push-Location $InstallDir
try {
    & $Py -m PyInstaller --noconfirm --clean --onefile `
        --name install-helper `
        --distpath $PublishRoot `
        --workpath $HelperBuildDir `
        --specpath $BuildDir `
        $HelperSrc
    if ($LASTEXITCODE -ne 0) { throw "Helper PyInstaller failed (exit $LASTEXITCODE)" }
} finally {
    Pop-Location
}
if (-not (Test-Path -LiteralPath $HelperExe)) {
    throw "Build failed: $HelperExe not found"
}

# --- resources (same rules as build_publish.ps1) ---
$ResDst = Join-Path $PublishRoot "resources"
$ragHuge = "modelica_doc_index.json"
Write-Host "Sync resources -> publish (robocopy; omit $ragHuge; /XD generated)..." -ForegroundColor DarkGray
$resSrcFull = (Resolve-Path -LiteralPath $ResSrc).Path
New-Item -ItemType Directory -Path $ResDst -Force | Out-Null
$resRoboLog = Join-Path $env:TEMP ("robocopy_resources_exe_" + [Guid]::NewGuid().ToString("n") + ".log")
$sw = [Diagnostics.Stopwatch]::StartNew()
$null = & robocopy $resSrcFull $ResDst /E /XD generated /XF $ragHuge @script:RoboRetry @script:RoboQuiet /LOG:$resRoboLog
$resRoboRc = $LASTEXITCODE
$sw.Stop()
Write-Host "  robocopy finished in $($sw.Elapsed.TotalSeconds.ToString('0.0'))s (exit=$resRoboRc)" -ForegroundColor DarkGray
if ($resRoboRc -ge 8) {
    Write-Host "  robocopy reported errors; repairing missing/mismatched files..." -ForegroundColor Yellow
}
$skipGen = { param([string]$full)
    if ($full -match '\\generated\\') { return $true }
    return $false
}
Repair-MissingResourceFilesAfterRobocopy -SourceRoot $resSrcFull -DestRoot $ResDst -ExcludeFileName $ragHuge -SkipPath $skipGen
$nResSrc = @(Get-ChildItem -LiteralPath $ResSrc -Recurse -Force -File -ErrorAction Stop | Where-Object {
        $_.Name -ne $ragHuge -and -not (& $skipGen $_.FullName)
    }).Count
$nResDst = @(Get-ChildItem -LiteralPath $ResDst -Recurse -Force -File -ErrorAction Stop | Where-Object {
        $_.Name -ne $ragHuge -and -not (& $skipGen $_.FullName)
    }).Count
if ($nResSrc -ne $nResDst) {
    if ($resRoboRc -ge 8) { Write-RobocopyLogTail -LogPath $resRoboLog }
    throw "resources file count mismatch: src=$nResSrc dst=$nResDst"
}

# --- install scripts + README ---
Write-Host "Copy install scripts and README..." -ForegroundColor DarkGray
Copy-Item -LiteralPath $InstallScriptSrc -Destination (Join-Path $PublishRoot "install_mcp.ps1") -Force
if (Test-Path -LiteralPath $InstallScriptShSrc) {
    Copy-Item -LiteralPath $InstallScriptShSrc -Destination (Join-Path $PublishRoot "install_mcp.sh") -Force
}
if (Test-Path -LiteralPath $InstallMcpSilentSrc) {
    Copy-Item -LiteralPath $InstallMcpSilentSrc -Destination (Join-Path $PublishRoot "install_mcp_silent.py") -Force
}

$distInstallPs1 = Join-Path $PublishRoot "install_mcp.ps1"
$ps1Text = [System.IO.File]::ReadAllText($distInstallPs1, [System.Text.UTF8Encoding]::new($false))
if ($ps1Text.Length -gt 0 -and [int][char]$ps1Text[0] -eq 0xFEFF) { $ps1Text = $ps1Text.Substring(1) }
$utf8Bom = New-Object System.Text.UTF8Encoding($true)
[System.IO.File]::WriteAllText($distInstallPs1, $ps1Text, $utf8Bom)

Copy-Item -LiteralPath $ReadmeSrc -Destination (Join-Path $PublishRoot "README.md") -Force

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

Write-Host "Done. Output: $PublishRoot  ($versionDisplayPub)" -ForegroundColor Green
Write-Host "  exe: $Exe" -ForegroundColor Green
exit 0
