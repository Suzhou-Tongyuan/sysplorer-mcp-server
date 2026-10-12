<#
.SYNOPSIS
  在 install/.venv 创建虚拟环境，安装依赖后用 PyInstaller 打包 sysplorer_mcp_server.exe 到仓库根目录 dist/。
.NOTES
  - mworks.sysplorer / pywin32 等需已进入当前 venv；通常从本机 Sysplorer 自带 Python 环境安装同名包到 .venv。
  - 可选环境变量 MWORKS_SYSPLORER_PYTHON：指向 Sysplorer 的 python.exe，脚本会尝试用其 -m pip 向 .venv 安装 mworks / pywin32（若存在对应 wheel）。
  - 仓库根 resources/ 同步到 dist/resources/：先删除 dist/resources 再 Copy-Item -LiteralPath 整树复制（完整替换）；同步后校验文件/目录数量。目录内任意新增/更新文件（含 modeling_skills/ 下 Markdown）均随整树一并发布，无需改 .spec。脚本不使用顶层 [CmdletBinding]，避免与部分 PS 版本组合时出现 AmbiguousParameterSet。
  - 全部完成后在 dist/ 生成发布包：sysplorer_mcp_server_v{versionFull}.7z（已安装 7-Zip 时），否则为同名 .zip；打包前会删除 dist 内既有 sysplorer_mcp_server_v*.7z/.zip，避免旧包被打进新归档；先写入 %TEMP% 再移入 dist，避免归档把正在生成的新包打进去。versionFull 与 MCP_BUILD_INFO / exe 一致。
  - 版本：`install/package_version.json` 的 `version_base`（如 0.6）；内部版（默认）为 `0.6.x`，x=`git rev-list --count HEAD`；加 `-Release` 时仅 `0.6`（与 `install/build_publish.ps1` 发布目录一致）。
#>
param(
    [string]$RepoRoot = "",
    [string]$MworksSysplorerPython = $env:MWORKS_SYSPLORER_PYTHON,
    [switch]$Release
)

function Invoke-QuietPip {
    param([string]$PythonExe, [string[]]$Args)
    $old = $ErrorActionPreference
    $ErrorActionPreference = "SilentlyContinue"
    try {
        & $PythonExe -X utf8 -m pip @Args 1>$null 2>$null
    } finally {
        $ErrorActionPreference = $old
    }
}

function Copy-MworksSitePackages {
    param(
        [Parameter(Mandatory = $true)][string]$MworksInstallDir,
        [Parameter(Mandatory = $true)][string]$VenvSitePackages
    )
    $src = Join-Path $MworksInstallDir "External\python64\Lib\site-packages"
    if (-not (Test-Path $src)) {
        Write-Warning "Sysplorer site-packages not found: $src"
        return
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

function New-VenvWithCandidates {
    param(
        [Parameter(Mandatory = $true)][string]$VenvDir,
        [string[]]$Candidates
    )
    foreach ($candidate in $Candidates) {
        if ([string]::IsNullOrWhiteSpace($candidate)) { continue }
        try {
            if ($candidate -eq "py -3.12") {
                & py -3.12 -m venv $VenvDir 2>$null
            } else {
                & $candidate -m venv $VenvDir 2>$null
            }
        } catch {
        }
        if (Test-Path (Join-Path $VenvDir "Scripts\python.exe")) {
            return $true
        }
    }
    return $false
}

$ErrorActionPreference = "Stop"
$InstallDir = $PSScriptRoot

function Test-PyImport {
    param([string]$PythonExe, [string]$Code)
    $prev = $ErrorActionPreference
    $ErrorActionPreference = "SilentlyContinue"
    try {
        $out = & $PythonExe -c $Code 2>$null
        return ($out -match "ok")
    } finally {
        $ErrorActionPreference = $prev
    }
}

function Get-SevenZipExe {
    $pf86 = ${env:ProgramFiles(x86)}
    foreach ($p in @(
        (Join-Path $env:ProgramFiles "7-Zip\7z.exe"),
        $(if ($pf86) { Join-Path $pf86 "7-Zip\7z.exe" })
    )) {
        if ($p -and (Test-Path -LiteralPath $p)) { return $p }
    }
    $cmd = Get-Command 7z.exe -ErrorAction SilentlyContinue
    if ($cmd -and $cmd.Source) { return [string]$cmd.Source }
    return $null
}

if (-not $RepoRoot) {
    $RepoRoot = (Resolve-Path (Join-Path $InstallDir "..")).Path
} else {
    $RepoRoot = (Resolve-Path $RepoRoot).Path
}
$VenvDir = Join-Path $InstallDir ".venv"
$DistDir = Join-Path $RepoRoot "dist"
$BuildDir = Join-Path $InstallDir "build"
$ReqFile = Join-Path $InstallDir "requirements-build.txt"
$SpecFile = Join-Path $InstallDir "windows\sysplorer_mcp_server.spec"

Write-Host "Repo root: $RepoRoot"
Write-Host "Venv:      $VenvDir"
Write-Host "Output:    $DistDir"

if (-not (Test-Path $ReqFile)) { throw "Missing $ReqFile" }
if (-not (Test-Path $SpecFile)) { throw "Missing $SpecFile" }

# --- 1) venv ---
if (-not (Test-Path (Join-Path $VenvDir "Scripts\python.exe"))) {
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    $venvCreated = New-VenvWithCandidates -VenvDir $VenvDir -Candidates @(
        $MworksSysplorerPython,
        "py -3.12",
        "python"
    )
    if (-not $venvCreated) {
        throw "Failed to create virtual environment in $VenvDir"
    }
}
$Py = Join-Path $VenvDir "Scripts\python.exe"
if (-not (Test-Path $Py)) { throw "python.exe not found in $VenvDir" }

function Invoke-VenvPip {
    param([string[]]$PipArgs)
    & $Py -X utf8 -m pip @PipArgs
}

Invoke-VenvPip -PipArgs @("install", "--upgrade", "pip")
Invoke-VenvPip -PipArgs @("install", "-r", $ReqFile)

# mworks-sysplorer 通常不在公共 PyPI；尝试静默安装（失败则忽略）
Write-Host "Trying pip install mworks-sysplorer (optional)..." -ForegroundColor DarkGray
Invoke-QuietPip -PythonExe $Py -Args @("install", "mworks-sysplorer")

# 自动猜测 Sysplorer 自带 Python
if (-not $MworksSysplorerPython -and $env:MWORKS_INSTALL_DIR) {
    $guess = Join-Path $env:MWORKS_INSTALL_DIR "External\python64\python.exe"
    if (Test-Path $guess) { $MworksSysplorerPython = $guess }
}

# --- 2) 可选：用 Sysplorer 自带 Python 的 pip 写入本 venv site-packages ---
$site = Join-Path $VenvDir "Lib\site-packages"
if ($MworksSysplorerPython -and (Test-Path $MworksSysplorerPython)) {
    Write-Host "pip install --target venv via: $MworksSysplorerPython" -ForegroundColor Cyan
    Invoke-QuietPip -PythonExe $MworksSysplorerPython -Args @("install", "--upgrade", "pip")
    Invoke-QuietPip -PythonExe $MworksSysplorerPython -Args @("install", "--target", $site, "mworks-sysplorer", "pywin32")
}

# pip 装不上时，直接从 Sysplorer 安装目录复制 API 包（与官方「自带 Python」一致）
if (-not (Test-PyImport -PythonExe $Py -Code "import mworks.sysplorer; print('ok')")) {
    if ($env:MWORKS_INSTALL_DIR -and (Test-Path $env:MWORKS_INSTALL_DIR)) {
        Copy-MworksSitePackages -MworksInstallDir $env:MWORKS_INSTALL_DIR -VenvSitePackages $site
        # 复制出来的 mworks 仍可能依赖未随包复制的三方模块
        Invoke-VenvPip -PipArgs @("install", "websocket-client", "jsonrpcclient", "psutil") 2>$null | Out-Null
    }
}

# --- 3) 检查 mworks.sysplorer（PyInstaller collect_all 需要）---
if (-not (Test-PyImport -PythonExe $Py -Code "import mworks.sysplorer; print('ok')")) {
    $probe = @"
try:
    import mworks.sysplorer
    print('ok')
except Exception as e:
    print('fail', e)
"@
    $prev = $ErrorActionPreference
    $ErrorActionPreference = "SilentlyContinue"
    $check = & $Py -c $probe 2>&1 | Out-String
    $ErrorActionPreference = $prev
    Write-Warning @"
未能在 .venv 中 import mworks.sysplorer。请设置环境变量 MWORKS_INSTALL_DIR 为 Sysplorer 根目录后重试（脚本会复制 External\python64\Lib\site-packages 下的 mworks*），或手动:
  & '$Py' -m pip install mworks-sysplorer
当前探测输出: $check
"@
    throw "Prerequisite: mworks.sysplorer not importable in venv."
}

# --- 3b) 版本：package_version.json + write_build_meta.py（供 PyInstaller 打入 exe）---
$WriteMeta = Join-Path $InstallDir "write_build_meta.py"
if (-not (Test-Path -LiteralPath $WriteMeta)) { throw "Missing $WriteMeta" }
$PkgVerJson = Join-Path $InstallDir "package_version.json"
if (-not (Test-Path -LiteralPath $PkgVerJson)) { throw "Missing $PkgVerJson" }

$mode = if ($Release) { "release" } else { "internal" }
$buildInfoJson = & $Py $WriteMeta --repo-root $RepoRoot --mode $mode --print-json
if ($LASTEXITCODE -ne 0) { throw "write_build_meta.py failed (exit $LASTEXITCODE)" }
$buildInfo = $buildInfoJson | ConvertFrom-Json
$versionFull = [string]$buildInfo.version
$versionDisplay = [string]$buildInfo.version_display
if ([string]::IsNullOrWhiteSpace($versionDisplay)) { $versionDisplay = $versionFull }
$versionCore = [string]$buildInfo.version_base
$counter = [int]$buildInfo.build_counter
$buildTime = [string]$buildInfo.build_time
$gitRev = [string]$buildInfo.git_revision
$buildKind = [string]$buildInfo.build_kind

Write-Host "Version: $versionDisplay | Build time: $buildTime | Git: $gitRev" -ForegroundColor Cyan

# --- 4) PyInstaller ---
$PyInstaller = Join-Path $VenvDir "Scripts\pyinstaller.exe"
if (-not (Test-Path $PyInstaller)) { throw "pyinstaller.exe not found in venv" }

New-Item -ItemType Directory -Path $DistDir -Force | Out-Null
New-Item -ItemType Directory -Path $BuildDir -Force | Out-Null

Push-Location $InstallDir
try {
    & $PyInstaller --noconfirm --clean `
        --distpath $DistDir `
        --workpath $BuildDir `
        $SpecFile
} finally {
    Pop-Location
}

$Exe = Join-Path $DistDir "sysplorer_mcp_server.exe"
if (-not (Test-Path $Exe)) {
    throw "Build failed: $Exe not found"
}

# --- 5) 旁置 resources + install/windows/README.md + install 脚本（与 path_config 一致）---
# 完整替换：先删 dist/resources，再 -LiteralPath 整树复制（避免目标侧残留旧文件；Copy-Item 使用解析后的源路径）。
$ResSrc = Join-Path $RepoRoot "resources"
$ResDst = Join-Path $DistDir "resources"
if (Test-Path -LiteralPath $ResSrc) {
    $resSrcFull = (Resolve-Path -LiteralPath $ResSrc).Path
    # 避免 Split-Path -LiteralPath -Parent 在部分 PS 版本上报 AmbiguousParameterSet
    $resDstParent = [System.IO.Path]::GetDirectoryName($ResDst)
    if ($resDstParent -and -not (Test-Path -LiteralPath $resDstParent)) {
        New-Item -ItemType Directory -Path $resDstParent -Force | Out-Null
    }
    Write-Host "Copying resources (full replace) -> $ResDst" -ForegroundColor Cyan
    if (Test-Path -LiteralPath $ResDst) {
        Remove-Item -LiteralPath $ResDst -Recurse -Force
    }
    Copy-Item -LiteralPath $resSrcFull -Destination $ResDst -Recurse -Force
    if (-not (Test-Path -LiteralPath $ResDst)) {
        throw "Resources destination missing after sync: $ResDst"
    }
    # 体积可达数百 MB，默认不随包分发（运行时可用 MCP_RAG_INDEX_PATH / 旁置 resources 自建索引）
    $ragHuge = "modelica_doc_index.json"
    Get-ChildItem -LiteralPath $ResDst -Recurse -Force -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -eq $ragHuge } |
        ForEach-Object {
            Write-Host "Omitting large RAG index from dist: $($_.Name)" -ForegroundColor DarkYellow
            Remove-Item -LiteralPath $_.FullName -Force -ErrorAction Stop
        }
    $nResSrc = @(Get-ChildItem -LiteralPath $ResSrc -Recurse -Force -File -ErrorAction Stop | Where-Object { $_.Name -ne $ragHuge }).Count
    $nResDst = @(Get-ChildItem -LiteralPath $ResDst -Recurse -Force -File -ErrorAction Stop | Where-Object { $_.Name -ne $ragHuge }).Count
    if ($nResSrc -ne $nResDst) {
        throw "resources sync check failed: file count src=$nResSrc dst=$nResDst ($ResSrc -> $ResDst)"
    }
    $dResSrc = @(Get-ChildItem -LiteralPath $ResSrc -Recurse -Force -Directory -ErrorAction SilentlyContinue).Count
    $dResDst = @(Get-ChildItem -LiteralPath $ResDst -Recurse -Force -Directory -ErrorAction SilentlyContinue).Count
    if ($dResSrc -ne $dResDst) {
        throw "resources sync check failed: directory count src=$dResSrc dst=$dResDst ($ResSrc -> $ResDst)"
    }
    Write-Host "Resources sync OK: $nResSrc files, $dResSrc directories" -ForegroundColor DarkGray
}

$ReadmePublishSrc = Join-Path $InstallDir "windows\README.md"
$Extras = @(
    @{ Src = $ReadmePublishSrc; DstName = "README.md" },
    @{ Src = (Join-Path $InstallDir "dist\install_mcp.ps1"); DstName = "install_mcp.ps1" }
)
foreach ($item in $Extras) {
    $src = $item.Src
    if (Test-Path -LiteralPath $src) {
        Copy-Item -LiteralPath $src -Destination (Join-Path $DistDir $item.DstName) -Force
    }
}
if (-not (Test-Path -LiteralPath (Join-Path $DistDir "README.md"))) {
    throw "Missing install/windows/README.md for dist bundle: $ReadmePublishSrc"
}

# install_mcp.ps1: Windows PowerShell 5.1 needs UTF-8 BOM to parse non-ASCII in the script reliably
$distInstallPs1 = Join-Path $DistDir "install_mcp.ps1"
if (Test-Path $distInstallPs1) {
    $ps1Text = [System.IO.File]::ReadAllText($distInstallPs1, [System.Text.UTF8Encoding]::new($false))
    if ($ps1Text.Length -gt 0 -and [int][char]$ps1Text[0] -eq 0xFEFF) { $ps1Text = $ps1Text.Substring(1) }
    $utf8Bom = New-Object System.Text.UTF8Encoding($true)
    [System.IO.File]::WriteAllText($distInstallPs1, $ps1Text, $utf8Bom)
}

$BuildInfoPath = Join-Path $DistDir "MCP_BUILD_INFO.json"
$buildInfoObj = [ordered]@{
    version            = $versionFull
    version_display    = $versionDisplay
    version_base       = $versionCore
    version_core       = $versionCore
    build_counter      = $counter
    git_commit_count   = [int]$buildInfo.git_commit_count
    build_kind         = $buildKind
    build_time         = $buildTime
    git_revision       = $gitRev
}
($buildInfoObj | ConvertTo-Json -Depth 5) | Set-Content -Path $BuildInfoPath -Encoding UTF8
Write-Host "Wrote $BuildInfoPath" -ForegroundColor DarkGray

# 删除 dist 内历史发布包，避免下面打包 dist\* 时把旧 .7z/.zip 嵌进新归档
Get-ChildItem -LiteralPath $DistDir -Force -File -ErrorAction SilentlyContinue |
    Where-Object {
        $_.Name -like 'sysplorer_mcp_server_v*.7z' -or $_.Name -like 'sysplorer_mcp_server_v*.zip'
    } |
    ForEach-Object {
        Write-Host "Removing old release archive: $($_.Name)" -ForegroundColor DarkGray
        Remove-Item -LiteralPath $_.FullName -Force -ErrorAction Stop
    }

# --- 6) dist 发布包：sysplorer_mcp_server_v{versionFull}.7z / .zip ---
# 输出必须在 dist 内，但源为 dist\*，故先打包到 %TEMP% 再 Move-Item，避免把正在生成的压缩包打进归档。
$archiveBaseName = "sysplorer_mcp_server_v$versionFull"
$distResolved = (Resolve-Path -LiteralPath $DistDir).Path
$sevenZip = Get-SevenZipExe
if ($sevenZip) {
    $archiveFinal = Join-Path $DistDir "$archiveBaseName.7z"
    $tempArchive = Join-Path $env:TEMP ("sysplorer_mcp_pack_" + [Guid]::NewGuid().ToString("n") + ".7z")
    try {
        Write-Host "Creating archive (7z): $archiveFinal" -ForegroundColor Cyan
        & $sevenZip a -t7z -mx=5 -bso0 -bsp1 -y $tempArchive "$distResolved\*"
        if ($LASTEXITCODE -ne 0) {
            throw "7-Zip failed (exit $LASTEXITCODE): $archiveFinal"
        }
        if (Test-Path -LiteralPath $archiveFinal) {
            Remove-Item -LiteralPath $archiveFinal -Force
        }
        Move-Item -LiteralPath $tempArchive -Destination $archiveFinal -Force
    }
    finally {
        if (Test-Path -LiteralPath $tempArchive) {
            Remove-Item -LiteralPath $tempArchive -Force -ErrorAction SilentlyContinue
        }
    }
    Write-Host "Archive: $archiveFinal" -ForegroundColor Green
}
else {
    $archiveFinal = Join-Path $DistDir "$archiveBaseName.zip"
    $tempArchive = Join-Path $env:TEMP ("sysplorer_mcp_pack_" + [Guid]::NewGuid().ToString("n") + ".zip")
    try {
        Write-Host "7-Zip not found; creating zip: $archiveFinal" -ForegroundColor Yellow
        Compress-Archive -Path (Join-Path $distResolved '*') -DestinationPath $tempArchive -Force
        if (Test-Path -LiteralPath $archiveFinal) {
            Remove-Item -LiteralPath $archiveFinal -Force
        }
        Move-Item -LiteralPath $tempArchive -Destination $archiveFinal -Force
    }
    finally {
        if (Test-Path -LiteralPath $tempArchive) {
            Remove-Item -LiteralPath $tempArchive -Force -ErrorAction SilentlyContinue
        }
    }
    Write-Host "Archive: $archiveFinal" -ForegroundColor Green
}

Write-Host "Done: $Exe ($versionDisplay)" -ForegroundColor Green
