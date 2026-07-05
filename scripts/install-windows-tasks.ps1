# scripts/install-windows-tasks.ps1
# 注册 2 个 Windows 任务计划程序任务：
#   AI-Berkshire-Portfolio-Weekly  每周日 03:00 跑 portfolio-review
#   AI-Berkshire-Industry-Monthly  每月 1 号 03:00 跑 industry-funnel --from-queue
#
# 默认凌晨 3 点跑：GLM Coding Plan 是 5 小时刷新套餐，凌晨使用不挤占白天配额。
#
# 用法：
#   pwsh -ExecutionPolicy Bypass -File scripts/install-windows-tasks.ps1
#   pwsh -ExecutionPolicy Bypass -File scripts/install-windows-tasks.ps1 -RunAt "04:00"
#
# 卸载：scripts/uninstall-windows-tasks.ps1
#
# 用 schtasks 命令而非 Register-ScheduledTask：schtasks 跨 PowerShell 版本兼容性更好，
# 直接支持 /sc weekly /sc monthly 触发器。

param(
    [string]$RepoRoot = "C:\workspace\ai-berkshire",
    [string]$RunAt = "03:00"
)

$ErrorActionPreference = "Stop"

# 校验仓库根目录
if (-not (Test-Path "$RepoRoot\tools\scheduler\__main__.py")) {
    Write-Error "Missing $RepoRoot\tools\scheduler\__main__.py"
    exit 2
}

$entryScript = "$RepoRoot\scripts\run-scheduled-task.ps1"
if (-not (Test-Path $entryScript)) {
    Write-Error "Missing $entryScript"
    exit 2
}

# schtasks /tr 参数：完整命令行（含引号需要小心转义）
# 跑 powershell 调 run-scheduled-task.ps1，-Skill 决定跑哪个 skill
$taskRunner = "powershell.exe -ExecutionPolicy Bypass -NoProfile -File `"$entryScript`" -Skill `"%SKILL%`""

# --- 任务 1：portfolio-review 周日 03:00 ---
$task1Name = "AI-Berkshire-Portfolio-Weekly"
$runner1 = $taskRunner -replace "%SKILL%", "portfolio-review"
schtasks /create /tn $task1Name /tr $runner1 /sc weekly /d Sun /st $RunAt /f
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to register $task1Name (exit=$LASTEXITCODE)"
    exit 1
}
Write-Host "[OK] $task1Name  (every Sunday $RunAt)"

# --- 任务 2：industry-funnel 每月 1 号 03:00 ---
$task2Name = "AI-Berkshire-Industry-Monthly"
$runner2 = $taskRunner -replace "%SKILL%", "industry-funnel"
schtasks /create /tn $task2Name /tr $runner2 /sc monthly /d 1 /st $RunAt /f
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to register $task2Name (exit=$LASTEXITCODE)"
    exit 1
}
Write-Host "[OK] $task2Name  (every 1st of month $RunAt)"

Write-Host ""
Write-Host "Verify:"
Write-Host "  schtasks /query /tn `"AI-Berkshire-*`" /v"
Write-Host ""
Write-Host "Trigger now (test):"
Write-Host "  schtasks /run /tn `"$task1Name`""
Write-Host ""
Write-Host "Uninstall:"
Write-Host "  pwsh -ExecutionPolicy Bypass -File scripts/uninstall-windows-tasks.ps1"
