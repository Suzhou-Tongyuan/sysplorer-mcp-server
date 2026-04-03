#Requires -Version 5.1
<#
.SYNOPSIS
Configure Claude / OpenCode / Codex CLI MCP to run sysplorer_mcp via Sysplorer bundled Python and a launcher main.py next to this script.
.PARAMETER MworksInstallDir
    Sysplorer installation root (used only for python.exe and --mworks-install-dir). If omitted, you are prompted (with a default path).
.NOTES
    main.py / sysplorer-mcp-server / resources must sit in the same folder as this install script. That bundle path is written to MCP config as an absolute path and does not depend on Sysplorer's install location (any directory is fine, not only Tools/sysplorer_mcp).
#>
param(
    [string]$MworksInstallDir = $null
)

$ErrorActionPreference = "Continue"

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

function Write-CodexSysplorerMcpToml([string]$configPath, [string]$command, [string[]]$mcpArgs) {
    $codexDir = Split-Path -Parent $configPath
    if (-not (Test-Path -LiteralPath $codexDir)) {
        New-Item -ItemType Directory -Path $codexDir -Force | Out-Null
    }
    $body = ""
    if (Test-Path -LiteralPath $configPath) {
        $body = [System.IO.File]::ReadAllText($configPath, [System.Text.UTF8Encoding]::new($false))
    }
    $body = Remove-McpServersTomlBlock $body "sysplorer_mcp"
    $body = Remove-McpServersTomlBlock $body "mworks_mcp"
    $sb = New-Object System.Text.StringBuilder
    [void]$sb.AppendLine("[mcp_servers.sysplorer_mcp]")
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

# $true = pip list 中含名为 mcp 的包；$false = 已找到 python 但列表中无 mcp；$null = 未找到解释器或 pip list 失败
function Test-SysplorerPythonPipListContainsMcp([string]$MworksInstallDir) {
    $py = Join-Path $MworksInstallDir "External\python64\python.exe"
    if (-not (Test-Path -LiteralPath $py)) { return $null }
    $oldEap = $ErrorActionPreference
    $ErrorActionPreference = "SilentlyContinue"
    $pipOut = & $py -m pip list 2>&1
    $pipExit = $LASTEXITCODE
    $ErrorActionPreference = $oldEap
    if ($pipExit -ne 0) { return $null }
    foreach ($item in $pipOut) {
        $line = "$item".Trim()
        if ($line -match '^\s*mcp\s+') { return $true }
    }
    return $false
}

function Write-SysplorerMcpPipCheckResult([string]$MworksInstallDir) {
    $py = Join-Path $MworksInstallDir "External\python64\python.exe"
    Write-Host "`n4. 正在检查 Sysplorer 自带 Python（pip list）中是否包含 mcp..." -ForegroundColor Yellow
    $mcpOk = Test-SysplorerPythonPipListContainsMcp -MworksInstallDir $MworksInstallDir
    if ($mcpOk -eq $true) {
        Write-Host "[OK] pip list 中已检测到 mcp 包。" -ForegroundColor Green
    } elseif ($mcpOk -eq $false) {
        Write-Host "当前选择的 Sysplorer 自带 Python 中未检测到 mcp 库。" -ForegroundColor Yellow
        Write-Host "请使用下列命令安装（PowerShell 中必须以 & 调用带空格路径下的解释器）：" -ForegroundColor Yellow
        Write-Host ("  & `"{0}`" -m pip install mcp" -f $py) -ForegroundColor Cyan
    } else {
        if (-not (Test-Path -LiteralPath $py)) {
            Write-Warning "未找到 Sysplorer 自带 Python，已跳过 mcp 检查: $py"
        } else {
            Write-Warning "无法执行 pip list 或无法解析结果，请手动确认是否已安装 mcp。"
        }
    }
}

# MCP 包根：仅由本脚本所在目录决定（绝对路径），与 Sysplorer 安装路径无关
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

$mainPy = Join-Path $scriptDir "main.py"
$pkgDir = Join-Path $scriptDir "sysplorer-mcp-server"
$resDir = Join-Path $scriptDir "resources"

if (-not (Test-Path -LiteralPath $mainPy)) {
    Write-Host "Error: main.py not found next to this install script." -ForegroundColor Red
    Write-Host "Expected at: $mainPy" -ForegroundColor Red
    Write-Host "Bundle root: $scriptDir (place main.py, sysplorer-mcp-server/, resources/ here; path is not derived from Sysplorer install dir)." -ForegroundColor Yellow
    Write-Host "Run install/build_publish.ps1 to populate publish/sysplorer_mcp, then copy that folder anywhere you like." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}
if (-not (Test-Path -LiteralPath $pkgDir)) {
    Write-Host "Error: sysplorer-mcp-server folder not found next to this script." -ForegroundColor Red
    Write-Host "Expected at: $pkgDir" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
if (-not (Test-Path -LiteralPath $resDir)) {
    Write-Host "Error: resources folder not found next to this script." -ForegroundColor Red
    Write-Host "Expected at: $resDir" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

$mainPyFull = (Resolve-Path -LiteralPath $mainPy).Path

$infoPath = Join-Path $scriptDir "MCP_BUILD_INFO.json"
if (Test-Path -LiteralPath $infoPath) {
    try {
        $rawInfo = [System.IO.File]::ReadAllText($infoPath, [System.Text.UTF8Encoding]::new($false))
        $pkgInfo = $rawInfo | ConvertFrom-Json
        Write-Host "-----------------------------------------------" -ForegroundColor DarkCyan
        $pkgVerShow = $pkgInfo.version_display
        if ([string]::IsNullOrWhiteSpace($pkgVerShow)) { $pkgVerShow = $pkgInfo.version }
        Write-Host " Current package version: $pkgVerShow" -ForegroundColor Green
        Write-Host " Build time:              $($pkgInfo.build_time)" -ForegroundColor Green
        if ($pkgInfo.git_revision -and ($pkgInfo.git_revision -ne "unknown")) {
            Write-Host " Git revision:            $($pkgInfo.git_revision)" -ForegroundColor DarkGray
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

Write-Host "=== MWorks MCP (Sysplorer Python) Configuration ===" -ForegroundColor Cyan
Write-Host "Bundle root (from this script): $scriptDir" -ForegroundColor Gray
Write-Host "main.py (written to MCP config):  $mainPyFull`n" -ForegroundColor Gray

$defaultMworksDir = "C:\Program Files\MWORKS\Sysplorer 2026a"
$mworksDir = $MworksInstallDir
if ([string]::IsNullOrWhiteSpace($mworksDir)) {
    $mworksDir = Read-Host "Enter Sysplorer installation path (default: $defaultMworksDir)"
}
if ([string]::IsNullOrWhiteSpace($mworksDir)) {
    $mworksDir = $defaultMworksDir
}

if (-not (Test-Path -LiteralPath $mworksDir)) {
    Write-Warning "Warning: The specified path $mworksDir does not exist, please confirm if it is correct"
    $continue = Read-Host "Continue? (Y/N, default Y)"
    if ($continue -eq "N" -or $continue -eq "n") {
        exit 0
    }
}

$pythonExe = Join-Path $mworksDir "External\python64\python.exe"
if (-not (Test-Path -LiteralPath $pythonExe)) {
    Write-Host "Error: Sysplorer bundled Python not found." -ForegroundColor Red
    Write-Host "Expected at: $pythonExe" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

$defaultPlatformLabel = "Sysplorer 2026a"
$platformLabel = Read-Host "Enter Sysplorer platform label (default: $defaultPlatformLabel)"
if ([string]::IsNullOrWhiteSpace($platformLabel)) {
    $platformLabel = $defaultPlatformLabel
}

Write-Host "`nUsing configuration:" -ForegroundColor Yellow
Write-Host "Sysplorer Path: $mworksDir"
Write-Host "Python:         $pythonExe"
Write-Host "Platform Label: $platformLabel`n"

$claudeConfigPath = Join-Path $env:USERPROFILE ".claude.json"
$opencodeConfigDir = Join-Path $env:USERPROFILE ".config\opencode"
$opencodeConfigPath = Join-Path $opencodeConfigDir "opencode.json"
$codexHome = if (-not [string]::IsNullOrWhiteSpace($env:HOME)) { $env:HOME } elseif (-not [string]::IsNullOrWhiteSpace($env:USERPROFILE)) { $env:USERPROFILE } else { (Resolve-Path ~).Path }
$codexConfigPath = Join-Path (Join-Path $codexHome ".codex") "config.toml"

Write-Host "0. Backing up existing configuration files (if any)..." -ForegroundColor Yellow
Backup-ConfigFileIfExists $claudeConfigPath
Backup-ConfigFileIfExists $opencodeConfigPath
Backup-ConfigFileIfExists $codexConfigPath
Write-Host ""

# 1. Configure Claude (.claude.json)
Write-Host "1. Configuring Claude..." -ForegroundColor Yellow

if (Test-Path -LiteralPath $claudeConfigPath) {
    $rawClaude = [System.IO.File]::ReadAllText($claudeConfigPath, [System.Text.UTF8Encoding]::new($false))
    $claudeConfig = $rawClaude | ConvertFrom-Json
} else {
    $claudeConfig = [PSCustomObject]@{}
}

if (-not $claudeConfig.mcpServers) {
    $claudeConfig | Add-Member -MemberType NoteProperty -Name "mcpServers" -Value ([PSCustomObject]@{}) -Force
}

$ms = $claudeConfig.mcpServers
if ($ms -and ($ms.PSObject.Properties.Name -contains 'mworks_mcp')) {
    $ms.PSObject.Properties.Remove('mworks_mcp')
}

$claudeConfig.mcpServers | Add-Member -MemberType NoteProperty -Name "sysplorer_mcp" -Value ([PSCustomObject]@{
    command = $pythonExe
    args = @(
        $mainPyFull,
        "--mworks-install-dir", $mworksDir,
        "--sysplorer-platform-label", $platformLabel
    )
}) -Force

$jsonContent = $claudeConfig | ConvertTo-Json -Depth 10
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($claudeConfigPath, $jsonContent, $utf8NoBom)
Write-Host "[OK] Claude configuration updated: $claudeConfigPath" -ForegroundColor Green

# 2. Configure OpenCode (opencode.json)
Write-Host "`n2. Configuring OpenCode..." -ForegroundColor Yellow

if (-not (Test-Path -LiteralPath $opencodeConfigDir)) {
    New-Item -ItemType Directory -Path $opencodeConfigDir -Force | Out-Null
}

if (Test-Path -LiteralPath $opencodeConfigPath) {
    $rawOpen = [System.IO.File]::ReadAllText($opencodeConfigPath, [System.Text.UTF8Encoding]::new($false))
    $opencodeConfig = $rawOpen | ConvertFrom-Json
} else {
    $opencodeConfig = [PSCustomObject]@{}
}

if (-not $opencodeConfig.mcp) {
    $opencodeConfig | Add-Member -MemberType NoteProperty -Name "mcp" -Value ([PSCustomObject]@{}) -Force
}

$mcpBlock = $opencodeConfig.mcp
if ($mcpBlock -and ($mcpBlock.PSObject.Properties.Name -contains 'mworks_mcp')) {
    $mcpBlock.PSObject.Properties.Remove('mworks_mcp')
}

$opencodeConfig.mcp | Add-Member -MemberType NoteProperty -Name "sysplorer_mcp" -Value ([PSCustomObject]@{
    type = "local"
    command = @(
        $pythonExe,
        $mainPyFull,
        "--mworks-install-dir", $mworksDir,
        "--sysplorer-platform-label", $platformLabel
    )
}) -Force

$jsonContent = $opencodeConfig | ConvertTo-Json -Depth 10
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($opencodeConfigPath, $jsonContent, $utf8NoBom)
Write-Host "[OK] OpenCode configuration updated: $opencodeConfigPath" -ForegroundColor Green

# 3. Configure Codex CLI (~/.codex/config.toml)
Write-Host "`n3. Configuring Codex CLI..." -ForegroundColor Yellow
Write-CodexSysplorerMcpToml -configPath $codexConfigPath -command $pythonExe -mcpArgs @(
    $mainPyFull,
    "--mworks-install-dir", $mworksDir,
    "--sysplorer-platform-label", $platformLabel
)
Write-Host "[OK] Codex configuration updated: $codexConfigPath" -ForegroundColor Green

Write-SysplorerMcpPipCheckResult -MworksInstallDir $mworksDir

Write-Host "`nConfiguration completed." -ForegroundColor Cyan
Write-Host "Please restart Claude Code / OpenCode / Codex CLI to load the new MCP configuration." -ForegroundColor Gray
Write-Host "Other Python deps (fastmcp, anyio, ...) may still be required in Sysplorer's site-packages; use the same python.exe -m pip if needed." -ForegroundColor Gray
Write-Host "To uninstall, remove the sysplorer_mcp entry from the corresponding configuration file." -ForegroundColor Gray
Read-Host "Press Enter to close"
