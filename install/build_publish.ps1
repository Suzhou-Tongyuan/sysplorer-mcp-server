<#
.SYNOPSIS
  Fill publish/sysplorer_mcp: launcher main.py, sysplorer-mcp-server (minus caches/tests), resources, install_mcp.ps1, MCP_BUILD_INFO.json, README.md (from install/windows/README.md); then zip that folder.
.NOTES
  Output layout matches Sysplorer Tools/sysplorer_mcp.
  resources/ 为整树复制至 publish 包内；modeling_skills/ 等下新增或更新的 Markdown 无需单独列入复制清单。
  sysplorer-mcp-server 下 temp/、logs/ 为本地运行残留，发布时 /XD 排除，避免被占用或权限导致 robocopy 失败/假死。
  若长时间停在「Sync resources」：多为杀软扫描大索引 JSON（如 indexes/sysblock_model_library_index.json）、或个别文件被占用；脚本会打印 robocopy 日志路径，失败时自动 tail 日志；请先关闭占用 publish/resources 或源 resources 的进程后再跑。
  目录填充完成后，将 publish/sysplorer_mcp 打成 zip 放到 publish/：sysplorer_mcp_v{version}.zip。打包前删除 publish/ 下既有 sysplorer_mcp_v*.zip；先写入 %TEMP% 再移入 publish，避免把压缩包打进自身。
  默认发布版：版本号仅为 install/package_version.json 的 version_base（如 0.6）。
  加 -Internal：内部版 version_base.x（x = git rev-list --count HEAD）。
  均写入 publish 内 sysplorer-mcp-server/_build_meta.py 与 MCP_BUILD_INFO.json。
  启动后会提示手动输入 Python（>= 3.10）的 python.exe 路径并校验；也可用 -PythonExe 跳过交互直接校验。
#>
param(
    [string]$RepoRoot = "",
    [string]$PythonExe = "",
    [switch]$Internal
)

$ErrorActionPreference = "Stop"

function Resolve-PublishPythonExe {
    <#
    .SYNOPSIS
      交互输入（或使用 -PythonExe）并校验 python.exe 可用。
    #>
    param(
        [string]$PythonExeHint = "",
        [Version]$MinVersion = [Version]"3.10.0"
    )
    $path = ""
    if (-not [string]::IsNullOrWhiteSpace($PythonExeHint)) {
        $path = $PythonExeHint.Trim().Trim([char]34).Trim([char]39)
        Write-Host ("使用参数 -PythonExe: {0}" -f $path) -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "=== Python 路径 ===" -ForegroundColor Cyan
        Write-Host "请输入本机 Python 3.10+ 的 python.exe 完整路径（例如 D:\Python310\python.exe）" -ForegroundColor Cyan
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
    $verText = "{0}.{1}.{2}" -f $Matches[1], $Matches[2], $Matches[3]
    try {
        $ver = [Version]$verText
    } catch {
        throw ("Python 校验失败：版本号无法解析 '{0}'（{1}）" -f $verText, $resolved)
    }
    if ($ver -lt $MinVersion) {
        throw ("Python 版本过低: {0}（需要 >= {1}）: {2}" -f $verText, $MinVersion, $resolved)
    }
    Write-Host "Python 校验通过: $resolved" -ForegroundColor Green
    Write-Host "  version:    $verText" -ForegroundColor DarkGray
    return $resolved
}

# robocopy 默认 /R 约 100 万次；遇被占用或杀软拦截时会长时间假死。发布脚本用有限重试（总等待仍可能达数分钟，见各步耗时输出）。
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
      若仍无法移走（如进程锁定 logs\server.log 且拒绝一切重命名/移动），返回 $false，供调用方做就地合并复制。
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
        Write-Host "  (renamed locked folder to $staleName — remove when idle)" -ForegroundColor Yellow
        return $true
    } catch {
        Write-Host "  (rename-away failed: $($_.Exception.Message))" -ForegroundColor Yellow
    }
    if (-not (Test-Path -LiteralPath $Path)) { return $true }
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
        throw "Cannot remove publish folder: $Path`nClose programs using files under this path, then retry.`nTip: logs or indexes under publish may be locked by a running MCP or antivirus."
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
    <#
    .SYNOPSIS
      Some hosts (AV / controlled folder) make CopyFile/robocopy fail on certain .mo with ERROR 5 while ReadAllBytes+WriteAllBytes succeeds.
    #>
    param([string]$SourceFile, [string]$DestFile)
    if (-not (Test-Path -LiteralPath $SourceFile)) { return }
    $dir = Split-Path -Parent $DestFile
    if (-not (Test-Path -LiteralPath $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    try {
        $bytes = [System.IO.File]::ReadAllBytes($SourceFile)
        [System.IO.File]::WriteAllBytes($DestFile, $bytes)
    } catch {
        Write-Host "  warn: byte fallback copy failed: $SourceFile -> $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

function Repair-MissingResourceFilesAfterRobocopy {
    <#
    .SYNOPSIS
      robocopy 在部分环境下会对个别 .mo 等文件报失败（exit>=8），而 ReadAllBytes+WriteAllBytes 仍可用。
      按与发布包相同的排除规则扫描源树：目标缺失或字节数不一致则字节回退复制，避免维护硬编码路径列表。
    #>
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
            try {
                $dl = (Get-Item -LiteralPath $destFile).Length
                if ($dl -ne $_.Length) { $need = $true }
            } catch {
                $need = $true
            }
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

function Get-LegacyChineseManualFileName {
    # UTF-8 bytes for: 安装部署手册.md (cleanup only; ASCII-safe in PS 5.1)
    [System.Text.Encoding]::UTF8.GetString([byte[]]@(
        0xE5, 0xAE, 0x89, 0xE8, 0xA3, 0x85, 0xE9, 0x83, 0xA8, 0xE7, 0xBD, 0xB2, 0xE6, 0x89, 0x8B, 0xE5, 0x86, 0x8C, 0x2E, 0x6D, 0x64
    ))
}

if (-not $RepoRoot) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
} else {
    $RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
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

$PythonExe = Resolve-PublishPythonExe -PythonExeHint $PythonExe

Write-Host "Repo:    $RepoRoot" -ForegroundColor Cyan
Write-Host "Publish: $PublishRoot" -ForegroundColor Cyan
Write-Host "Python:  $PythonExe" -ForegroundColor Cyan
Write-Host "Mode:    $metaMode" -ForegroundColor Cyan

New-Item -ItemType Directory -Path $PublishRoot -Force | Out-Null

Write-Host "Copy launcher (main.py)..." -ForegroundColor DarkGray
Copy-Item -LiteralPath $LauncherSrc -Destination (Join-Path $PublishRoot "main.py") -Force

$ServerDst = Join-Path $PublishRoot "sysplorer-mcp-server"
Write-Host "Sync sysplorer-mcp-server -> publish (robocopy /R:2 /W:1)..." -ForegroundColor DarkGray
$serverMergeIntoExisting = $false
if (Test-Path -LiteralPath $ServerDst) {
    $swP = [Diagnostics.Stopwatch]::StartNew()
    $cleared = Try-ClearDirectoryForReplace -Path $ServerDst
    if (-not $cleared) {
        $serverMergeIntoExisting = $true
        Write-Host "  could not replace target folder (often logs\server.log locked by MCP); merging copy into existing tree - stop MCP for a fully clean bundle next time" -ForegroundColor Yellow
    }
    Write-Host "  prepared sysplorer-mcp-server target in $($swP.Elapsed.TotalSeconds.ToString('0.0'))s" -ForegroundColor DarkGray
}
if (-not (Test-Path -LiteralPath $ServerDst)) {
    New-Item -ItemType Directory -Path $ServerDst -Force | Out-Null
}
$robolog = Join-Path $env:TEMP ("robocopy_publish_" + [Guid]::NewGuid().ToString("n") + ".log")
Write-Host "  robocopy log: $robolog" -ForegroundColor DarkGray
$sw = [Diagnostics.Stopwatch]::StartNew()
$null = & robocopy $ServerSrc $ServerDst /E /XD __pycache__ tests .pytest_cache temp logs /XF *.pyc /XF modelica_doc_index.json @script:RoboRetry @script:RoboQuiet /LOG:$robolog
$sw.Stop()
Write-Host "  robocopy finished in $($sw.Elapsed.TotalSeconds.ToString('0.0'))s (exit=$LASTEXITCODE)" -ForegroundColor DarkGray
if ($LASTEXITCODE -ge 8) { Write-RobocopyLogTail -LogPath $robolog }
Assert-RobocopyExitCode -Rc $LASTEXITCODE -What "sysplorer-mcp-server (log: $robolog)"

$ResDst = Join-Path $PublishRoot "resources"
$ragHuge = "modelica_doc_index.json"
$dependencySkillDir = "modeling_skills\ty-sysplorer-dependency-guard"
Write-Host "Sync resources -> publish (omit $ragHuge; exclude generated and model-library dependency skill; include CAD skill)..." -ForegroundColor DarkGray
if (Test-Path -LiteralPath $ResDst) {
    $swP = [Diagnostics.Stopwatch]::StartNew()
    Remove-TreeBestEffort -Path $ResDst
    Write-Host "  purged old resources in $($swP.Elapsed.TotalSeconds.ToString('0.0'))s" -ForegroundColor DarkGray
}
$resSrcFull = (Resolve-Path -LiteralPath $ResSrc).Path
$dependencyRoot = Join-Path $resSrcFull $dependencySkillDir
New-Item -ItemType Directory -Path $ResDst -Force | Out-Null
$resRoboLog = Join-Path $env:TEMP ("robocopy_resources_" + [Guid]::NewGuid().ToString("n") + ".log")
Write-Host "  robocopy log: $resRoboLog" -ForegroundColor DarkGray
$sw = [Diagnostics.Stopwatch]::StartNew()
# /XD generated：省略可再生的 Sysblock 代码生成示例目录，缩短复制并减少杀软对 .c/.h 的扫描；需要时可在安装后按 skill 自行生成
$resRoboRc = 0
$null = & robocopy $resSrcFull $ResDst /E /XD generated $dependencyRoot /XF $ragHuge @script:RoboRetry @script:RoboQuiet /LOG:$resRoboLog
$resRoboRc = $LASTEXITCODE
$sw.Stop()
Write-Host "  robocopy finished in $($sw.Elapsed.TotalSeconds.ToString('0.0'))s (exit=$resRoboRc)" -ForegroundColor DarkGray
if ($resRoboRc -ge 8) {
    Write-Host "  robocopy reported errors; repairing missing/mismatched files (byte fallback, AV/CopyFile quirk)..." -ForegroundColor Yellow
}
$skipGen = { param([string]$full)
    if ($full -match '\\generated\\') { return $true }
    $dependencyRoot = Join-Path $resSrcFull $dependencySkillDir
    if ($full.StartsWith($dependencyRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { return $true }
    return $false
}
Repair-MissingResourceFilesAfterRobocopy -SourceRoot $resSrcFull -DestRoot $ResDst -ExcludeFileName $ragHuge -SkipPath $skipGen
Write-Host "Verify resources file counts (exclude $ragHuge and **\generated\**, same as robocopy /XD)..." -ForegroundColor DarkGray
$nResSrc = @(Get-ChildItem -LiteralPath $ResSrc -Recurse -Force -File -ErrorAction Stop | Where-Object {
        $_.Name -ne $ragHuge -and -not (& $skipGen $_.FullName)
    }).Count
$nResDst = @(Get-ChildItem -LiteralPath $ResDst -Recurse -Force -File -ErrorAction Stop | Where-Object {
        $_.Name -ne $ragHuge -and -not (& $skipGen $_.FullName)
    }).Count
if ($nResSrc -ne $nResDst) {
    if ($resRoboRc -ge 8) { Write-RobocopyLogTail -LogPath $resRoboLog }
    throw "resources file count mismatch: src=$nResSrc dst=$nResDst (see robocopy log if printed above)"
}
if ($resRoboRc -ge 8) {
    Write-Host "  note: robocopy exit was $resRoboRc but file counts match after fallback / verify." -ForegroundColor DarkGray
}

Write-Host "Copy install scripts..." -ForegroundColor DarkGray
Copy-Item -LiteralPath $InstallScriptSrc -Destination (Join-Path $PublishRoot "install_mcp.ps1") -Force
Copy-Item -LiteralPath $InstallScriptShSrc -Destination (Join-Path $PublishRoot "install_mcp.sh") -Force
$InstallMcpSilentSrc = Join-Path $InstallDir "install_mcp_silent.py"
if (-not (Test-Path -LiteralPath $InstallMcpSilentSrc)) {
    throw "Missing install_mcp_silent.py: $InstallMcpSilentSrc"
}
Copy-Item -LiteralPath $InstallMcpSilentSrc -Destination (Join-Path $PublishRoot "install_mcp_silent.py") -Force

$distInstallPs1 = Join-Path $PublishRoot "install_mcp.ps1"
$ps1Text = [System.IO.File]::ReadAllText($distInstallPs1, [System.Text.UTF8Encoding]::new($false))
if ($ps1Text.Length -gt 0 -and [int][char]$ps1Text[0] -eq 0xFEFF) { $ps1Text = $ps1Text.Substring(1) }
$utf8Bom = New-Object System.Text.UTF8Encoding($true)
[System.IO.File]::WriteAllText($distInstallPs1, $ps1Text, $utf8Bom)

Write-Host "Write build metadata (write_build_meta.py)..." -ForegroundColor DarkGray
$metaDst = Join-Path $ServerDst "_build_meta.py"
$buildInfoJson = & $PythonExe $WriteMeta --repo-root $RepoRoot --mode $metaMode --output $metaDst --print-json 2>$null
if ($LASTEXITCODE -ne 0) {
    throw "write_build_meta.py failed (exit $LASTEXITCODE) via $PythonExe"
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

# 将 publish/sysplorer_mcp 打成 zip，放到 publish/（与目录并列，不把压缩包打进目录内）
$PublishParent = Join-Path $RepoRoot "publish"
$archiveFinal = Join-Path $PublishParent ("sysplorer_mcp_v{0}.zip" -f [string]$buildInfo.version)
Get-ChildItem -LiteralPath $PublishParent -Force -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -like 'sysplorer_mcp_v*.zip' } |
    ForEach-Object {
        Write-Host "Removing old publish archive: $($_.Name)" -ForegroundColor DarkGray
        Remove-Item -LiteralPath $_.FullName -Force -ErrorAction Stop
    }

$publishResolved = (Resolve-Path -LiteralPath $PublishRoot).Path
$tempArchive = Join-Path $env:TEMP ("sysplorer_mcp_publish_" + [Guid]::NewGuid().ToString("n") + ".zip")
try {
    Write-Host "Creating zip: $archiveFinal" -ForegroundColor Cyan
    Compress-Archive -Path $publishResolved -DestinationPath $tempArchive -Force
    Move-Item -LiteralPath $tempArchive -Destination $archiveFinal -Force
} finally {
    if (Test-Path -LiteralPath $tempArchive) {
        Remove-Item -LiteralPath $tempArchive -Force -ErrorAction SilentlyContinue
    }
}
Write-Host "Archive: $archiveFinal" -ForegroundColor Green

Write-Host "Done. Output: $PublishRoot  ($versionDisplayPub)" -ForegroundColor Green
