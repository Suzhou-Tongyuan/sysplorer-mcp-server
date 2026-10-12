#Requires -Version 5.1
<#
.SYNOPSIS
Configure Claude / OpenCode / Codex CLI / Mogick MCP to run sysplorer via sysplorer_mcp_server.exe next to this script.
.PARAMETER MworksInstallDir
    Sysplorer installation root (passed as --mworks-install-dir to the exe). Alias: -d.
.PARAMETER SysplorerPlatformLabel
    Value for --sysplorer-platform-label written into MCP client configs. Alias: -p.
    modelica-lite packs default to modelica_lite.
.PARAMETER UserWorkspace
    Optional --user-workspace for model-library download/install (modelica_lite). Alias: -w.
.NOTES
    Silent / non-interactive install: pass -p (and -d unless this is a modelica-lite pack),
    or set env SYSPLORER_PLATFORM_LABEL / MWORKS_INSTALL_DIR.
    sysplorer_mcp_server.exe / resources must sit in the same folder as this install script.
#>
param(
    [Alias("d")]
    [string]$MworksInstallDir = $null,
    [Alias("p")]
    [string]$SysplorerPlatformLabel = $null,
    [Alias("w")]
    [string]$UserWorkspace = $null
)

if ([string]::IsNullOrWhiteSpace($MworksInstallDir) -and -not [string]::IsNullOrWhiteSpace($env:MWORKS_INSTALL_DIR)) {
    $MworksInstallDir = $env:MWORKS_INSTALL_DIR
}
if ([string]::IsNullOrWhiteSpace($SysplorerPlatformLabel) -and -not [string]::IsNullOrWhiteSpace($env:SYSPLORER_PLATFORM_LABEL)) {
    $SysplorerPlatformLabel = $env:SYSPLORER_PLATFORM_LABEL
}
if ([string]::IsNullOrWhiteSpace($UserWorkspace) -and -not [string]::IsNullOrWhiteSpace($env:MCP_USER_WORKSPACE_DIR)) {
    $UserWorkspace = $env:MCP_USER_WORKSPACE_DIR
}

# Avoid blocking Read-Host on errors when the caller passed platform (typical silent / lite install).
$silentInstall = -not [string]::IsNullOrWhiteSpace($SysplorerPlatformLabel)

$ErrorActionPreference = "Continue"
$McpClientKey = "sysplorer"
$LegacyMcpKeys = @("sysplorer_mcp", "mworks_mcp")
$OpenCodeMcpTimeoutMs = 600000
$MogickMcpTimeoutMs = 1000000
$McpExeName = "sysplorer_mcp_server.exe"

function Escape-TomlSingleQuoted([string]$s) {
    if ($null -eq $s) { return "" }
    return ($s -replace "'", "''")
}

function Remove-McpServersTomlBlock([string]$text, [string]$serverKey) {
    $header = "[mcp_servers.$serverKey]"
    $lines = [regex]::Split($text, '\r\n|\n|\r')
    $out = New-Object System.Collections.Generic.List[string]
    $i = 0
    while ($i -lt $lines.Count) {
        if ($lines[$i].Trim() -eq $header) {
            $i++
            while ($i -lt $lines.Count -and ($lines[$i] -notmatch '^\s*\[')) {
                $i++
            }
            continue
        }
        [void]$out.Add($lines[$i])
        $i++
    }
    return ($out -join [Environment]::NewLine)
}

function Remove-LegacyMcpKeys([PSCustomObject]$block) {
    if ($null -eq $block) { return }
    foreach ($key in $LegacyMcpKeys) {
        if ($block.PSObject.Properties.Name -contains $key) {
            $block.PSObject.Properties.Remove($key)
        }
    }
}

function Remove-AllMcpServersTomlBlocks([string]$text, [string]$serverKey) {
    $body = $text
    do {
        $prev = $body
        $body = Remove-McpServersTomlBlock $body $serverKey
    } while ($prev -ne $body)
    return $body
}

function Write-CodexSysplorerToml([string]$configPath, [string]$command, [string[]]$mcpArgs) {
    $codexDir = Split-Path -Parent $configPath
    if (-not (Test-Path -LiteralPath $codexDir)) {
        New-Item -ItemType Directory -Path $codexDir -Force | Out-Null
    }
    $body = ""
    if (Test-Path -LiteralPath $configPath) {
        $body = [System.IO.File]::ReadAllText($configPath, [System.Text.UTF8Encoding]::new($false))
    }
    foreach ($key in ($LegacyMcpKeys + @($McpClientKey))) {
        $body = Remove-AllMcpServersTomlBlocks $body $key
    }
    $sb = New-Object System.Text.StringBuilder
    [void]$sb.AppendLine("[mcp_servers.$McpClientKey]")
    [void]$sb.AppendLine(("command = '{0}'" -f (Escape-TomlSingleQuoted $command)))
    [void]$sb.AppendLine("args = [")
    foreach ($a in $mcpArgs) {
        [void]$sb.AppendLine(("    '{0}'," -f (Escape-TomlSingleQuoted $a)))
    }
    [void]$sb.AppendLine("]")
    $block = $sb.ToString()
    $body = $body.TrimEnd()
    if ($body.Length -gt 0) {
        $body = $body + [Environment]::NewLine + [Environment]::NewLine + $block
    } else {
        $body = $block
    }
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($configPath, $body.TrimEnd() + [Environment]::NewLine, $utf8NoBom)
}

function Backup-ConfigFileIfExists([string]$path) {
    if (-not (Test-Path -LiteralPath $path)) { return }
    $dir = [System.IO.Path]::GetDirectoryName($path)
    $leaf = [System.IO.Path]::GetFileName($path)
    $stamp = (Get-Date).ToString("yyyyMMdd-HHmmssfff")
    $backupName = "{0}.bak.{1}" -f $leaf, $stamp
    $backupPath = if ($dir) { Join-Path $dir $backupName } else { $backupName }
    Copy-Item -LiteralPath $path -Destination $backupPath -Force
    Write-Host "[OK] Backed up: $path -> $backupPath" -ForegroundColor DarkGray
}

function Read-JsonConfigRoot([string]$path) {
    if (-not (Test-Path -LiteralPath $path)) {
        return [PSCustomObject]@{}
    }
    $raw = [System.IO.File]::ReadAllText($path, [System.Text.UTF8Encoding]::new($false))
    if ([string]::IsNullOrWhiteSpace($raw)) {
        return [PSCustomObject]@{}
    }
    try {
        $obj = $raw | ConvertFrom-Json
    } catch {
        Write-Warning ("Could not parse JSON config {0}: {1}" -f $path, $_)
        return [PSCustomObject]@{}
    }
    if ($null -eq $obj -or $obj -isnot [System.Management.Automation.PSCustomObject]) {
        return [PSCustomObject]@{}
    }
    return $obj
}

function Ensure-ConfigNestedObject([PSCustomObject]$config, [string]$name) {
    $val = $config.$name
    if ($null -eq $val -or $val -isnot [System.Management.Automation.PSCustomObject]) {
        if ($config.PSObject.Properties.Name -contains $name) {
            $config.PSObject.Properties.Remove($name)
        }
        $nested = [PSCustomObject]@{}
        $config | Add-Member -MemberType NoteProperty -Name $name -Value $nested -Force
        return $nested
    }
    return $val
}

$scriptDir = $null
if ($MyInvocation.MyCommand.Path) {
    $scriptDir = Split-Path -Parent ([System.IO.Path]::GetFullPath($MyInvocation.MyCommand.Path))
}
if ([string]::IsNullOrWhiteSpace($scriptDir) -and -not [string]::IsNullOrWhiteSpace($PSScriptRoot)) {
    $scriptDir = [System.IO.Path]::GetFullPath($PSScriptRoot)
}
if ([string]::IsNullOrWhiteSpace($scriptDir)) {
    $scriptDir = (Get-Location -PSProvider FileSystem).Path
}

$mcpExe = Join-Path $scriptDir $McpExeName
$resDir = Join-Path $scriptDir "resources"

if (-not (Test-Path -LiteralPath $mcpExe)) {
    Write-Host "Error: $McpExeName not found next to this install script." -ForegroundColor Red
    Write-Host "Expected at: $mcpExe" -ForegroundColor Red
    Write-Host "Run install/build_publish_exe.ps1 to populate publish/sysplorer_mcp_exe." -ForegroundColor Yellow
    if (-not $silentInstall) { Read-Host "Press Enter to exit" }
    exit 1
}
if (-not (Test-Path -LiteralPath $resDir)) {
    Write-Host "Error: resources folder not found next to this script." -ForegroundColor Red
    Write-Host "Expected at: $resDir" -ForegroundColor Red
    if (-not $silentInstall) { Read-Host "Press Enter to exit" }
    exit 1
}

$mcpExeFull = (Resolve-Path -LiteralPath $mcpExe).Path
$mcpArgs = @(
    "--mworks-install-dir", "",
    "--sysplorer-platform-label", ""
)

$infoPath = Join-Path $scriptDir "MCP_BUILD_INFO.json"
$pkgInfo = $null
$packVariant = ""
if (Test-Path -LiteralPath $infoPath) {
    try {
        $rawInfo = [System.IO.File]::ReadAllText($infoPath, [System.Text.UTF8Encoding]::new($false))
        $pkgInfo = $rawInfo | ConvertFrom-Json
        if ($pkgInfo.pack_variant) { $packVariant = [string]$pkgInfo.pack_variant }
        Write-Host "-----------------------------------------------" -ForegroundColor DarkCyan
        $pkgVerShow = $pkgInfo.version_display
        if ([string]::IsNullOrWhiteSpace($pkgVerShow)) { $pkgVerShow = $pkgInfo.version }
        Write-Host " Current package version: $pkgVerShow" -ForegroundColor Green
        Write-Host " Build time:              $($pkgInfo.build_time)" -ForegroundColor Green
        if ($pkgInfo.git_revision -and ($pkgInfo.git_revision -ne "unknown")) {
            Write-Host " Git revision:            $($pkgInfo.git_revision)" -ForegroundColor DarkGray
        }
        if (-not [string]::IsNullOrWhiteSpace($packVariant)) {
            Write-Host " Pack variant:            $packVariant" -ForegroundColor DarkGray
        }
        Write-Host "-----------------------------------------------" -ForegroundColor DarkCyan
        Write-Host ""
    } catch {
        Write-Warning "Could not parse MCP_BUILD_INFO.json: $_"
        Write-Host ""
    }
} else {
    Write-Warning "MCP_BUILD_INFO.json not found next to this script; version/build time unknown."
    Write-Host ""
}

$isLitePack = $packVariant -in @("modelica_lite", "mols", "modelica-lite")
if ($isLitePack) {
    $silentInstall = -not [string]::IsNullOrWhiteSpace($SysplorerPlatformLabel)
} else {
    $silentInstall = (-not [string]::IsNullOrWhiteSpace($MworksInstallDir)) -and (-not [string]::IsNullOrWhiteSpace($SysplorerPlatformLabel))
}

Write-Host "=== MWorks MCP (PyInstaller exe) Configuration ===" -ForegroundColor Cyan
Write-Host "Bundle root (from this script): $scriptDir" -ForegroundColor Gray
Write-Host "MCP exe (written to MCP config): $mcpExeFull`n" -ForegroundColor Gray

$defaultMworksDir = if ($isLitePack) { "" } else { "C:\Program Files\MWORKS\Sysplorer 2026a" }
$defaultPlatformLabel = if ($isLitePack) { "modelica_lite" } else { "Sysplorer 2026b" }

$mworksDir = $MworksInstallDir
if ([string]::IsNullOrWhiteSpace($mworksDir) -and -not $silentInstall) {
    $prompt = if ($isLitePack) {
        "Enter Sysplorer/mols install path (optional, Enter to skip)"
    } else {
        "Enter Sysplorer installation path (default: $defaultMworksDir)"
    }
    $mworksDir = Read-Host $prompt
}
if ([string]::IsNullOrWhiteSpace($mworksDir) -and -not $isLitePack) {
    $mworksDir = $defaultMworksDir
}

if (-not [string]::IsNullOrWhiteSpace($mworksDir) -and -not (Test-Path -LiteralPath $mworksDir)) {
    Write-Warning "Warning: The specified path $mworksDir does not exist, please confirm if it is correct"
    if ($silentInstall) {
        Write-Host "[INFO] Silent install: continuing despite missing Sysplorer path." -ForegroundColor DarkGray
    } else {
        $continue = Read-Host "Continue? (Y/N, default Y)"
        if ($continue -eq "N" -or $continue -eq "n") {
            exit 0
        }
    }
}

$platformLabel = $SysplorerPlatformLabel
if ([string]::IsNullOrWhiteSpace($platformLabel) -and -not $silentInstall) {
    $platformLabel = Read-Host "Enter Sysplorer platform label (default: $defaultPlatformLabel)"
}
if ([string]::IsNullOrWhiteSpace($platformLabel)) {
    $platformLabel = $defaultPlatformLabel
}

$mcpArgs = @(
    "--mworks-install-dir", $(if ($mworksDir) { $mworksDir } else { "" }),
    "--sysplorer-platform-label", $platformLabel
)
if (-not [string]::IsNullOrWhiteSpace($UserWorkspace)) {
    $mcpArgs += @("--user-workspace", $UserWorkspace)
}

function Resolve-SkillsSyncPython {
    param([string]$MworksRoot)
    if (-not [string]::IsNullOrWhiteSpace($MworksRoot)) {
        $bundled = Join-Path $MworksRoot "External\python64\python.exe"
        if (Test-Path -LiteralPath $bundled) { return $bundled }
    }
    foreach ($cmd in @("py", "python", "python3")) {
        $hit = Get-Command $cmd -ErrorAction SilentlyContinue
        if ($null -eq $hit) { continue }
        if ($cmd -eq "py") { return $hit.Source }
        return $hit.Source
    }
    return $null
}

function Sync-BundledModelingSkillsFallback {
    param([string]$BundleRoot)
    $src = Join-Path $BundleRoot "resources\modeling_skills"
    if (-not (Test-Path -LiteralPath $src)) { return }
    $dests = @(
        (Join-Path $env:USERPROFILE ".config\opencode\skills"),
        (Join-Path $env:USERPROFILE ".mworks\mogick\Sysplorer\skills")
    )
    $retired = @("ty-sysplorer-modeling-router", "ty-cadtool-modeling", "sysplorer-mds-docs")
    $managed = @(Get-ChildItem -LiteralPath $src -Directory -ErrorAction SilentlyContinue | Where-Object {
            Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md")
        })
    foreach ($dest in $dests) {
        New-Item -ItemType Directory -Path $dest -Force | Out-Null
        foreach ($name in $retired) {
            $old = Join-Path $dest $name
            if (Test-Path -LiteralPath $old) {
                Remove-Item -LiteralPath $old -Recurse -Force -ErrorAction SilentlyContinue
            }
        }
        foreach ($sk in $managed) {
            $target = Join-Path $dest $sk.Name
            if (Test-Path -LiteralPath $target) {
                Remove-Item -LiteralPath $target -Recurse -Force
            }
            Copy-Item -LiteralPath $sk.FullName -Destination $target -Recurse -Force
        }
        Write-Host "[OK] Skills copied to $dest" -ForegroundColor Green
    }
}

$pythonExe = Resolve-SkillsSyncPython -MworksRoot $mworksDir

Write-Host "`nUsing configuration:" -ForegroundColor Yellow
Write-Host "Sysplorer Path: $(if ($mworksDir) { $mworksDir } else { '(not set)' })"
Write-Host "MCP exe:        $mcpExeFull"
Write-Host "Platform Label: $platformLabel"
if (-not [string]::IsNullOrWhiteSpace($UserWorkspace)) {
    Write-Host "User workspace: $UserWorkspace"
}
Write-Host ""

$claudeConfigPath = Join-Path $env:USERPROFILE ".claude.json"
$opencodeConfigDir = Join-Path $env:USERPROFILE ".config\opencode"
$opencodeConfigPath = Join-Path $opencodeConfigDir "opencode.json"
$codexHome = if (-not [string]::IsNullOrWhiteSpace($env:HOME)) { $env:HOME } elseif (-not [string]::IsNullOrWhiteSpace($env:USERPROFILE)) { $env:USERPROFILE } else { (Resolve-Path ~).Path }
$codexConfigPath = Join-Path (Join-Path $codexHome ".codex") "config.toml"
$mogickConfigDir = Join-Path $env:USERPROFILE ".mworks\mogick\Sysplorer"
$mogickConfigPath = Join-Path $mogickConfigDir "mcp.json"

Write-Host "0. Backing up existing configuration files (if any)..." -ForegroundColor Yellow
Backup-ConfigFileIfExists $claudeConfigPath
Backup-ConfigFileIfExists $opencodeConfigPath
Backup-ConfigFileIfExists $codexConfigPath
Backup-ConfigFileIfExists $mogickConfigPath
Write-Host ""

Write-Host "1. Configuring Claude..." -ForegroundColor Yellow
$claudeConfig = Read-JsonConfigRoot $claudeConfigPath
$ms = Ensure-ConfigNestedObject $claudeConfig "mcpServers"
Remove-LegacyMcpKeys $ms
$claudeConfig.mcpServers | Add-Member -MemberType NoteProperty -Name $McpClientKey -Value ([PSCustomObject]@{
    command = $mcpExeFull
    args = $mcpArgs
}) -Force
$jsonContent = $claudeConfig | ConvertTo-Json -Depth 10
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($claudeConfigPath, $jsonContent, $utf8NoBom)
Write-Host "[OK] Claude configuration updated: $claudeConfigPath" -ForegroundColor Green

Write-Host "`n2. Configuring OpenCode..." -ForegroundColor Yellow
if (-not (Test-Path -LiteralPath $opencodeConfigDir)) {
    New-Item -ItemType Directory -Path $opencodeConfigDir -Force | Out-Null
}
$opencodeConfig = Read-JsonConfigRoot $opencodeConfigPath
$mcpBlock = Ensure-ConfigNestedObject $opencodeConfig "mcp"
Remove-LegacyMcpKeys $mcpBlock
$opencodeCommand = @($mcpExeFull) + $mcpArgs
$opencodeConfig.mcp | Add-Member -MemberType NoteProperty -Name $McpClientKey -Value ([PSCustomObject]@{
    type = "local"
    command = $opencodeCommand
    timeout = $OpenCodeMcpTimeoutMs
}) -Force
$jsonContent = $opencodeConfig | ConvertTo-Json -Depth 10
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($opencodeConfigPath, $jsonContent, $utf8NoBom)
Write-Host "[OK] OpenCode configuration updated: $opencodeConfigPath" -ForegroundColor Green

Write-Host "`n3. Configuring Codex CLI..." -ForegroundColor Yellow
Write-CodexSysplorerToml -configPath $codexConfigPath -command $mcpExeFull -mcpArgs $mcpArgs
Write-Host "[OK] Codex configuration updated: $codexConfigPath" -ForegroundColor Green

Write-Host "`n4. Configuring Mogick..." -ForegroundColor Yellow
if (-not (Test-Path -LiteralPath $mogickConfigDir)) {
    New-Item -ItemType Directory -Path $mogickConfigDir -Force | Out-Null
}
$mogickConfig = Read-JsonConfigRoot $mogickConfigPath
$serversBlock = Ensure-ConfigNestedObject $mogickConfig "servers"
Remove-LegacyMcpKeys $serversBlock
$mogickConfig.servers | Add-Member -MemberType NoteProperty -Name $McpClientKey -Value ([PSCustomObject]@{
    type = "local"
    enabled = $true
    command = $opencodeCommand
    timeout = $MogickMcpTimeoutMs
}) -Force
$jsonContent = $mogickConfig | ConvertTo-Json -Depth 10
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($mogickConfigPath, $jsonContent, $utf8NoBom)
Write-Host "[OK] Mogick configuration updated: $mogickConfigPath" -ForegroundColor Green

Write-Host "`n5. MCP runtime is bundled in the exe; no separate pip install of mcp is required." -ForegroundColor DarkGray

$silentPy = Join-Path $scriptDir "install_mcp_silent.py"
if ($env:NO_SYNC_OPENCODE_SKILLS -eq "1") {
    Write-Host "`n[INFO] Skipping OpenCode skills sync (NO_SYNC_OPENCODE_SKILLS=1)." -ForegroundColor DarkGray
} elseif (Test-Path -LiteralPath $silentPy) {
    Write-Host "`nSyncing bundled modeling_skills to OpenCode / Mogick skills directories ..." -ForegroundColor Yellow
    $synced = $false
    if (-not [string]::IsNullOrWhiteSpace($pythonExe) -and (Test-Path -LiteralPath $pythonExe)) {
        try {
            if ((Split-Path -Leaf $pythonExe) -eq "py.exe") {
                & $pythonExe -3 $silentPy --sync-opencode-skills --bundle-root $scriptDir
            } else {
                & $pythonExe $silentPy --sync-opencode-skills --bundle-root $scriptDir
            }
            $synced = $true
        } catch {
            Write-Warning "Python skills sync failed: $_"
        }
    }
    if (-not $synced) {
        Write-Host "[INFO] No usable Python for skills sync; copying skill directories from the bundle." -ForegroundColor DarkGray
        Sync-BundledModelingSkillsFallback -BundleRoot $scriptDir
    }
} else {
    Write-Warning "install_mcp_silent.py not found next to this script; skipped OpenCode skills sync."
}

Write-Host "`nConfiguration completed." -ForegroundColor Cyan
Write-Host "Please restart Claude Code / OpenCode / Codex CLI / Mogick to load the new MCP configuration." -ForegroundColor Gray
Write-Host "To uninstall, remove the sysplorer entry from the corresponding configuration file." -ForegroundColor Gray
if (-not $silentInstall) {
    Read-Host "Press Enter to close"
}
