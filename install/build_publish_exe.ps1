<#
.SYNOPSIS
  使用指定 Python（>= 3.11）构建 PyInstaller exe，并填充 publish/sysplorer_mcp_exe（exe + resources + 安装脚本 + MCP_BUILD_INFO.json + README）。
.NOTES
  - 启动后会提示手动输入 Python（>= 3.11）的 python.exe 路径并校验；也可用 -PythonExe 跳过交互直接校验。
  - 默认输出：仓库 publish/sysplorer_mcp_exe/（与 build_publish.ps1 的 publish/sysplorer_mcp 并列）。
  - mworks.sysplorer 需可 import：设置 MWORKS_INSTALL_DIR，或 -MworksInstallDir，或脚本会从 E:\SysplorerSoftware 下自动探测。
  - 版本：默认发布版（version_base）；加 -Internal 为内部版 version_base.<git commit count>。
  - 本脚本产出给 modelica-lite / mols 的 exe 包（publish/sysplorer_mcp_exe）：宿主侧集成 sysplorer_mcp_server.exe，不依赖 Sysplorer Tools 目录式布局。
  - resources/ 先按 build_publish.ps1 规则同步（省略 modelica_doc_index.json、/XD generated），再叠加 resources_mogick/。
  - 与完整 Sysplorer 包的 skill 差异：排除 ty-cadtool-modeling、sysplorer-mds-docs、cad_toolbox_api；叠加 ty-sysplorer-dependency-guard 与 lite 版 modeling-rules。
#>
param(
    [string]$RepoRoot = "",
    [string]$PythonExe = "",
    [string]$MworksInstallDir = $env:MWORKS_INSTALL_DIR,
    [switch]$Internal
)

$ErrorActionPreference = "Stop"

function Wait-PublishScriptExit {
    param([string]$Message = "按 Enter 退出")
    if ($Host.Name -eq "ConsoleHost" -and [Environment]::UserInteractive) {
        try {
            if ([Console]::IsInputRedirected) { return }
        } catch { }
        Read-Host $Message | Out-Null
    }
}

trap {
    Write-Host ""
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Wait-PublishScriptExit
    break
}

function Resolve-PublishPythonExe {
    <#
    .SYNOPSIS
      交互输入（或使用 -PythonExe）并校验 python.exe 可用；exe 打包要求 Python >= 3.11。
    #>
    param(
        [string]$PythonExeHint = "",
        [int]$RequireMajor = 3,
        [int]$MinMinor = 11
    )
    $path = ""
    if (-not [string]::IsNullOrWhiteSpace($PythonExeHint)) {
        $path = $PythonExeHint.Trim().Trim([char]34).Trim([char]39)
        Write-Host ("使用参数 -PythonExe: {0}" -f $path) -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "=== Python 路径 ===" -ForegroundColor Cyan
        Write-Host ("请输入本机 Python {0}.{1}+ 的 python.exe 完整路径（例如 D:\Python311\python.exe）" -f $RequireMajor, $MinMinor) -ForegroundColor Cyan
        $raw = Read-Host "Python 路径"
        if ([string]::IsNullOrWhiteSpace($raw)) {
            throw "未输入 Python 路径，已中止打包。"
        }
        $path = $raw.Trim().Trim([char]34).Trim([char]39)
    }

    if (-not (Test-Path -LiteralPath $path)) {
        throw ("Python 路径不存在: {0}" -f $path)
    }
    $item = Get-Item -LiteralPath $path -ErrorAction Stop
    if ($item.PSIsContainer) {
        $candidate = Join-Path $path "python.exe"
        if (-not (Test-Path -LiteralPath $candidate)) {
            throw ("路径是目录且未找到 python.exe: {0}" -f $path)
        }
        Write-Host ("检测到目录，使用: {0}" -f $candidate) -ForegroundColor DarkGray
        $path = $candidate
    }
    $resolved = (Resolve-Path -LiteralPath $path).Path

    # 用 ProcessStartInfo 调用，避免 PS 5.1 对含空格路径 / -c 参数的错误拆分；
    # 同时避免 stderr 在 ErrorActionPreference=Stop 时被当成终止错误。
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $resolved
    $psi.Arguments = "--version"
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.CreateNoWindow = $true
    $proc = [System.Diagnostics.Process]::Start($psi)
    $stdout = $proc.StandardOutput.ReadToEnd()
    $stderr = $proc.StandardError.ReadToEnd()
    $proc.WaitForExit()
    $probeText = (($stdout + "`n" + $stderr).Trim())
    if ($proc.ExitCode -ne 0) {
        throw ("Python 校验失败（无法执行）: {0}`n{1}" -f $resolved, $probeText)
    }
    if ($probeText -notmatch 'Python\s+(\d+)\.(\d+)\.(\d+)') {
        throw ("Python 校验失败：未能读取版本信息: {0}`n{1}" -f $resolved, $probeText)
    }
    $major = [int]$Matches[1]
    $minor = [int]$Matches[2]
    $verText = "{0}.{1}.{2}" -f $Matches[1], $Matches[2], $Matches[3]
    if ($major -ne $RequireMajor -or $minor -lt $MinMinor) {
        throw ("exe 打包需要 Python {0}.{1}+，当前为 {2}: {3}" -f $RequireMajor, $MinMinor, $verText, $resolved)
    }
    Write-Host "Python 校验通过: $resolved" -ForegroundColor Green
    Write-Host "  version:    $verText" -ForegroundColor DarkGray
    return $resolved
}

$script:RoboQuiet = @("/NFL", "/NDL", "/NJH", "/NJS", "/nc", "/ns", "/np")
$script:RoboRetry = @("/R:2", "/W:1")

function Assert-RobocopyExitCode {
    param([int]$Rc, [string]$What)
    if ($Rc -ge 8) {
        throw "robocopy $What failed (exit $Rc)"
    }
}

function Try-ClearDirectoryForReplace {
    <#
    .SYNOPSIS
      清空目录以便写入全新内容：删除 → 同目录改名 → 空目录 robocopy 镜像清空 → 整树移到 %TEMP%。
      若仍无法移走（如进程锁定 exe），返回 $false。
    #>
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return $true }
    try {
        Remove-Item -LiteralPath $Path -Recurse -Force -ErrorAction Stop
        return $true
    } catch {
        Write-Host "  (Remove-Item failed: $($_.Exception.Message))" -ForegroundColor Yellow
    }
    if (-not (Test-Path -LiteralPath $Path)) { return $true }
    $leaf = Split-Path -Leaf $Path
    $staleName = $leaf + ".__publish_stale_" + [Guid]::NewGuid().ToString("n")
    try {
        Rename-Item -LiteralPath $Path -NewName $staleName -ErrorAction Stop
        Write-Host "  (renamed locked item to $staleName — remove when idle)" -ForegroundColor Yellow
        return $true
    } catch {
        Write-Host "  (rename-away failed: $($_.Exception.Message))" -ForegroundColor Yellow
    }
    if (-not (Test-Path -LiteralPath $Path)) { return $true }
    # Single file (e.g. locked .exe): try move to TEMP
    if (Test-Path -LiteralPath $Path -PathType Leaf) {
        try {
            $aside = Join-Path $env:TEMP ("mcp_publish_file_" + [Guid]::NewGuid().ToString("n") + "_" + $leaf)
            Move-Item -LiteralPath $Path -Destination $aside -ErrorAction Stop
            Write-Host "  (moved locked file to $aside — delete when free)" -ForegroundColor Yellow
            return $true
        } catch {
            Write-Host "  (move file to TEMP failed: $($_.Exception.Message))" -ForegroundColor Yellow
        }
        return $false
    }
    $empty = Join-Path $env:TEMP ("mcp_publish_empty_" + [Guid]::NewGuid().ToString("n"))
    try {
        New-Item -ItemType Directory -Path $empty -Force | Out-Null
        $null = & robocopy $empty $Path /MIR @script:RoboRetry @script:RoboQuiet
        $rc = $LASTEXITCODE
        if ($rc -lt 8) {
            try {
                Remove-Item -LiteralPath $Path -Force -Recurse -ErrorAction Stop
                return $true
            } catch {
                Write-Host "  (Remove-Item after purge: $($_.Exception.Message))" -ForegroundColor Yellow
            }
        } else {
            Write-Host "  (robocopy purge exit $rc)" -ForegroundColor Yellow
        }
    } finally {
        if (Test-Path -LiteralPath $empty) {
            Remove-Item -LiteralPath $empty -Force -Recurse -ErrorAction SilentlyContinue
        }
    }
    if (-not (Test-Path -LiteralPath $Path)) { return $true }
    try {
        $aside = Join-Path $env:TEMP ("mcp_publish_moved_" + [Guid]::NewGuid().ToString("n"))
        Move-Item -LiteralPath $Path -Destination $aside -ErrorAction Stop
        Write-Host "  (moved locked folder to $aside — delete when free)" -ForegroundColor Yellow
        return $true
    } catch {
        Write-Host "  (move to TEMP failed: $($_.Exception.Message))" -ForegroundColor Yellow
    }
    return $false
}

function Remove-TreeBestEffort {
    param([string]$Path)
    $ok = Try-ClearDirectoryForReplace -Path $Path
    if (-not $ok -and (Test-Path -LiteralPath $Path)) {
        throw ("Cannot remove publish item: {0}`nClose programs locking this path (often Cursor MCP still running sysplorer_mcp_server.exe), then retry." -f $Path)
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
            if ($n -lt 20) {
                Write-Host "  byte-fallback: $rel" -ForegroundColor DarkYellow
            } elseif ($n -eq 20) {
                Write-Host "  byte-fallback: ... (further files omitted)" -ForegroundColor DarkYellow
            }
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
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
} else {
    $RepoRoot = (Resolve-Path $RepoRoot).Path
}

$InstallDir = $PSScriptRoot
$PublishRoot = Join-Path $RepoRoot "publish\sysplorer_mcp_exe"
$VenvDir = Join-Path $InstallDir ".venv-exe-publish"
$BuildDir = Join-Path $InstallDir "build-exe-publish"
$HelperBuildDir = Join-Path $InstallDir "build-helper-publish"
$ReqFile = Join-Path $InstallDir "requirements-build.txt"
$SpecFile = Join-Path $InstallDir "windows\sysplorer_mcp_server.spec"
$HelperSrc = Join-Path $InstallDir "helpers\install_library_helper.py"
$WriteMeta = Join-Path $InstallDir "write_build_meta.py"
$PkgVerJson = Join-Path $InstallDir "package_version.json"
$ResSrc = Join-Path $RepoRoot "resources"
$MogickResSrc = Join-Path $RepoRoot "resources_mogick"
$ResourceStage = Join-Path $BuildDir "resources-staging"
$ReadmeSrc = Join-Path $InstallDir "windows\README_exe.md"
$InstallScriptSrc = Join-Path $InstallDir "windows\install_mcp_exe.ps1"
$InstallScriptShSrc = Join-Path $RepoRoot "install_mcp.sh"
$InstallMcpSilentSrc = Join-Path $InstallDir "install_mcp_silent.py"
$MetaDst = Join-Path $RepoRoot "sysplorer-mcp-server\_build_meta.py"

$PythonExe = Resolve-PublishPythonExe -PythonExeHint $PythonExe
if (-not (Test-Path -LiteralPath $ReqFile)) { throw "Missing $ReqFile" }
if (-not (Test-Path -LiteralPath $SpecFile)) { throw "Missing $SpecFile" }
if (-not (Test-Path -LiteralPath $HelperSrc)) { throw "Missing $HelperSrc" }
if (-not (Test-Path -LiteralPath $WriteMeta)) { throw "Missing $WriteMeta" }
if (-not (Test-Path -LiteralPath $PkgVerJson)) { throw "Missing $PkgVerJson" }
if (-not (Test-Path -LiteralPath $ResSrc)) { throw "Missing resources: $ResSrc" }
if (-not (Test-Path -LiteralPath $MogickResSrc)) { throw "Missing modelica-lite resources overlay: $MogickResSrc" }
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
# Soft-stop any MCP exe still using the previous publish output (Cursor often keeps it alive).
Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
    Where-Object {
        $_.Name -eq "sysplorer_mcp_server.exe" -and
        $_.CommandLine -and
        $_.CommandLine -like "*$PublishRoot*"
    } |
    ForEach-Object {
        Write-Host "  (stopping locked MCP pid $($_.ProcessId))" -ForegroundColor Yellow
        Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
    }
Start-Sleep -Milliseconds 400
New-Item -ItemType Directory -Path $PublishRoot -Force | Out-Null
Get-ChildItem -LiteralPath $PublishRoot -Force -ErrorAction SilentlyContinue | ForEach-Object {
    Remove-TreeBestEffort -Path $_.FullName
}

# --- venv ---
$venvPy = Join-Path $VenvDir "Scripts\python.exe"
$needNewVenv = $true
if (Test-Path -LiteralPath $venvPy) {
    $cfgPath = Join-Path $VenvDir "pyvenv.cfg"
    $cfgHome = ""
    $cfgExe = ""
    if (Test-Path -LiteralPath $cfgPath) {
        Get-Content -LiteralPath $cfgPath -ErrorAction SilentlyContinue | ForEach-Object {
            if ($_ -match '^\s*home\s*=\s*(.+)\s*$') { $cfgHome = $Matches[1].Trim() }
            if ($_ -match '^\s*executable\s*=\s*(.+)\s*$') { $cfgExe = $Matches[1].Trim() }
        }
    }
    $baseNorm = $PythonExe.TrimEnd('\')
    $cfgExeNorm = if ($cfgExe) { $cfgExe.TrimEnd('\') } else { "" }
    $cfgHomeNorm = if ($cfgHome) { $cfgHome.TrimEnd('\') } else { "" }
    $baseDir = Split-Path -Parent $baseNorm
    if (
        ($cfgExeNorm -and ([string]::Equals($cfgExeNorm, $baseNorm, [StringComparison]::OrdinalIgnoreCase))) -or
        ($cfgHomeNorm -and (
            [string]::Equals($cfgHomeNorm, $baseNorm, [StringComparison]::OrdinalIgnoreCase) -or
            [string]::Equals($cfgHomeNorm, $baseDir, [StringComparison]::OrdinalIgnoreCase)
        ))
    ) {
        $needNewVenv = $false
    } else {
        Write-Host "Existing venv base Python mismatch; recreating..." -ForegroundColor Yellow
        Write-Host ("  venv home/exe: {0} | {1}" -f $cfgHomeNorm, $cfgExeNorm) -ForegroundColor DarkGray
        Write-Host ("  selected:      {0}" -f $baseNorm) -ForegroundColor DarkGray
    }
}
if ($needNewVenv) {
    Write-Host "Creating venv with $PythonExe ..." -ForegroundColor Cyan
    if (Test-Path -LiteralPath $VenvDir) {
        Remove-TreeBestEffort -Path $VenvDir
    }
    & $PythonExe -m venv $VenvDir
    if (-not (Test-Path -LiteralPath $venvPy)) {
        throw "Failed to create venv at $VenvDir"
    }
}
$Py = $venvPy

function Invoke-VenvPip {
    param([string[]]$PipArgs)
    & $Py -X utf8 -m pip @PipArgs
    if ($LASTEXITCODE -ne 0) { throw "pip failed: $($PipArgs -join ' ')" }
}

Write-Host "Install build requirements..." -ForegroundColor DarkGray
Invoke-VenvPip -PipArgs @("install", "--upgrade", "pip")
Invoke-VenvPip -PipArgs @("install", "-r", $ReqFile)
# pywin32 must be installed by the venv interpreter itself (not Sysplorer --target),
# otherwise DLL/`__file__` lookup breaks PyInstaller hooks.
Invoke-VenvPip -PipArgs @("install", "--upgrade", "pywin32")
Invoke-QuietPip -PythonExePath $Py -Args @("install", "mworks-sysplorer")

$site = Join-Path $VenvDir "Lib\site-packages"
$mworksPy = if ($mworksDir) { Join-Path $mworksDir "External\python64\python.exe" } else { $null }
if ($mworksPy -and (Test-Path -LiteralPath $mworksPy)) {
    Write-Host "pip install --target venv via Sysplorer python (mworks only)..." -ForegroundColor Cyan
    Invoke-QuietPip -PythonExePath $mworksPy -Args @("install", "--upgrade", "pip")
    Invoke-QuietPip -PythonExePath $mworksPy -Args @("install", "--target", $site, "mworks-sysplorer")
}

if (-not (Test-PyImport -PythonExePath $Py -Code "import mworks.sysplorer; print('ok')")) {
    if ($mworksDir) {
        Copy-MworksSitePackages -MworksRoot $mworksDir -VenvSitePackages $site
    }
}

# Always ensure Sysplorer Python API base deps (offline_install.txt) for PyInstaller collect_all.
Invoke-VenvPip -PipArgs @("install", "websocket-client", "colorama", "jsonrpcclient", "psutil", "packaging")

if (-not (Test-PyImport -PythonExePath $Py -Code "import mworks.sysplorer; print('ok')")) {
    throw "Prerequisite: mworks.sysplorer not importable in venv. Set -MworksInstallDir or MWORKS_INSTALL_DIR to Sysplorer root, then retry."
}
if (-not (Test-PyImport -PythonExePath $Py -Code "import websocket, colorama, jsonrpcclient, psutil, packaging; print('ok')")) {
    throw "Prerequisite missing in venv: websocket/colorama/jsonrpcclient/psutil/packaging (Sysplorer Python API base deps)."
}
if (-not (Test-PyImport -PythonExePath $Py -Code "import pywintypes, win32api; print('ok')")) {
    throw "Prerequisite missing in venv: pywin32 (pywintypes/win32api). Re-run after deleting install\.venv-exe-publish."
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
$PyInstaller = Join-Path $VenvDir "Scripts\pyinstaller.exe"
if (-not (Test-Path -LiteralPath $PyInstaller)) { throw "pyinstaller.exe not found in venv" }
New-Item -ItemType Directory -Path $BuildDir -Force | Out-Null

Write-Host "PyInstaller -> $PublishRoot ..." -ForegroundColor Cyan
# Vendor mworks.sysplorer uses Windows path literals like "\Program ..."; Python 3.12 emits
# SyntaxWarning noise during analysis. Not a packaging failure — suppress for this step only.
$prevPyWarnings = $env:PYTHONWARNINGS
$env:PYTHONWARNINGS = "ignore::SyntaxWarning"
Push-Location $InstallDir
try {
    & $PyInstaller --noconfirm --clean `
        --distpath $PublishRoot `
        --workpath $BuildDir `
        $SpecFile
    if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed (exit $LASTEXITCODE)" }
} finally {
    Pop-Location
    if ($null -eq $prevPyWarnings) { Remove-Item Env:PYTHONWARNINGS -ErrorAction SilentlyContinue }
    else { $env:PYTHONWARNINGS = $prevPyWarnings }
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
    & $PyInstaller --noconfirm --clean --onefile `
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

# --- resources (modelica-lite: base resources + resources_mogick overlay) ---
$ResDst = Join-Path $PublishRoot "resources"
$ragHuge = "modelica_doc_index.json"
$liteExcludeRelDirs = @(
    "modeling_skills\ty-cadtool-modeling",
    "modeling_skills\sysplorer-mds-docs",
    "cad_toolbox_api"
)
$liteExcludeIndexNames = @("cad_toolbox_api_index.json")
Write-Host "Prepare modelica-lite resources staging (exclude CAD/MDS skills and CAD corpus; overlay dependency-guard)..." -ForegroundColor DarkGray
Remove-TreeBestEffort -Path $ResourceStage
New-Item -ItemType Directory -Path $ResourceStage -Force | Out-Null
$resRootFull = (Resolve-Path -LiteralPath $ResSrc).Path
$stageXd = @("generated")
foreach ($rel in $liteExcludeRelDirs) {
    $stageXd += (Join-Path $resRootFull $rel)
}
$stageRoboLog = Join-Path $env:TEMP ("robocopy_resources_stage_exe_" + [Guid]::NewGuid().ToString("n") + ".log")
$null = & robocopy $resRootFull $ResourceStage /E /XD @stageXd /XF $ragHuge @liteExcludeIndexNames @script:RoboRetry @script:RoboQuiet /LOG:$stageRoboLog
$stageRoboRc = $LASTEXITCODE
if ($stageRoboRc -ge 8) {
    Write-RobocopyLogTail -LogPath $stageRoboLog
    throw "resources staging copy failed (exit $stageRoboRc)"
}

$mogickRootFull = (Resolve-Path -LiteralPath $MogickResSrc).Path
$overlayRoboLog = Join-Path $env:TEMP ("robocopy_resources_mogick_exe_" + [Guid]::NewGuid().ToString("n") + ".log")
$null = & robocopy $mogickRootFull $ResourceStage /E @script:RoboRetry @script:RoboQuiet /LOG:$overlayRoboLog
$overlayRoboRc = $LASTEXITCODE
if ($overlayRoboRc -ge 8) {
    Write-RobocopyLogTail -LogPath $overlayRoboLog
    throw "resources_mogick overlay failed (exit $overlayRoboRc)"
}

Write-Host "Sync staged modelica-lite resources -> publish (robocopy; omit $ragHuge; /XD generated)..." -ForegroundColor DarkGray
$resSrcFull = (Resolve-Path -LiteralPath $ResourceStage).Path
New-Item -ItemType Directory -Path $ResDst -Force | Out-Null
$resRoboLog = Join-Path $env:TEMP ("robocopy_resources_exe_" + [Guid]::NewGuid().ToString("n") + ".log")
$sw = [Diagnostics.Stopwatch]::StartNew()
$null = & robocopy $resSrcFull $ResDst /E /XD generated /XF $ragHuge @liteExcludeIndexNames @script:RoboRetry @script:RoboQuiet /LOG:$resRoboLog
$resRoboRc = $LASTEXITCODE
$sw.Stop()
Write-Host "  robocopy finished in $($sw.Elapsed.TotalSeconds.ToString('0.0'))s (exit=$resRoboRc)" -ForegroundColor DarkGray
if ($resRoboRc -ge 8) {
    Write-Host "  robocopy reported errors; repairing missing/mismatched files..." -ForegroundColor Yellow
}
$skipGen = { param([string]$full)
    if ($full -match '\\generated\\') { return $true }
    foreach ($rel in $liteExcludeRelDirs) {
        $exRoot = Join-Path $resSrcFull $rel
        if ($full.StartsWith($exRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { return $true }
    }
    foreach ($xfName in $liteExcludeIndexNames) {
        if ([string]::Equals((Split-Path -Leaf $full), $xfName, [StringComparison]::OrdinalIgnoreCase)) { return $true }
    }
    return $false
}
Repair-MissingResourceFilesAfterRobocopy -SourceRoot $resSrcFull -DestRoot $ResDst -ExcludeFileName $ragHuge -SkipPath $skipGen
$nResSrc = @(Get-ChildItem -LiteralPath $resSrcFull -Recurse -Force -File -ErrorAction Stop | Where-Object {
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
    pack_variant       = "modelica_lite"
}
($buildInfoObj | ConvertTo-Json -Depth 5) | Set-Content -Path $BuildInfoPath -Encoding UTF8

Write-Host "Done. Output: $PublishRoot  ($versionDisplayPub)" -ForegroundColor Green
Write-Host "  exe: $Exe" -ForegroundColor Green
Wait-PublishScriptExit
exit 0
