# scripts/install-windows-tasks.ps1
# 注册 2 个 Windows 任务计划程序任务：
#   AI-Berkshire-Portfolio-Weekly  每周日 20:00 跑 portfolio-review
#   AI-Berkshire-Industry-Monthly  每月 1 号 20:00 跑 industry-funnel --from-queue
#
# 用法：
#   powershell -ExecutionPolicy Bypass -File scripts/install-windows-tasks.ps1
#
# 卸载：scripts/uninstall-windows-tasks.ps1
#
# 注意：以当前用户身份注册（交互登录态触发）。需要用户具有"作为批处理任务登录"权限，
#       一般桌面用户默认满足。

param(
    [string]$RepoRoot = "C:\workspace\ai-berkshire",
    [string]$RunAt = "20:00"
)

$ErrorActionPreference = "Stop"

# 校验仓库根目录
if (-not (Test-Path "$RepoRoot\tools\scheduler\__main__.py")) {
    Write-Error "找不到 $RepoRoot\tools\scheduler\__main__.py — RepoRoot 配置错？"
    exit 2
}

$entryScript = "$RepoRoot\scripts\run-scheduled-task.ps1"
if (-not (Test-Path $entryScript)) {
    Write-Error "找不到 $entryScript"
    exit 2
}

function Register-AiBerkshireTask {
    param(
        [string]$TaskName,
        [string]$SkillName,
        [string]$Description,
        [TimeSpan]$ExecutionTimeLimit
    )
    # Argument 是单个字符串：传给 powershell.exe 的所有参数
    $argStr = "-ExecutionPolicy Bypass -NoProfile -File `"$entryScript`" -Skill `"$SkillName`""
    $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument $argStr
    $settings = New-ScheduledTaskSettingsSet `
        -StartWhenAvailable `
        -DontStopOnIdleEnd `
        -ExecutionTimeLimit $ExecutionTimeLimit

    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $action `
        -Settings $settings `
        -Description $Description `
        -Force | Out-Null

    Write-Host "✅ 已注册：$TaskName"
}

# --- 任务 1：portfolio-review 周日 20:00 ---
Register-AiBerkshireTask `
    -TaskName "AI-Berkshire-Portfolio-Weekly" `
    -SkillName "portfolio-review" `
    -Description "AI Berkshire 周度：portfolio-review 我的持仓（自动更新 reports/portfolio-latest.md）" `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1)

# 单独再设触发器（Register-ScheduledTask 不支持在 splatting 里塞多个 trigger）
$task1 = Get-ScheduledTask -TaskName "AI-Berkshire-Portfolio-Weekly"
$task1.Triggers = @(New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At $RunAt)
Set-ScheduledTask -TaskName "AI-Berkshire-Portfolio-Weekly" -Trigger $task1.Triggers | Out-Null
Write-Host "   触发：每周 Sunday $RunAt"

# --- 任务 2：industry-funnel 每月 1 号 20:00 ---
Register-AiBerkshireTask `
    -TaskName "AI-Berkshire-Industry-Monthly" `
    -SkillName "industry-funnel" `
    -Description "AI Berkshire 月度：industry-funnel --from-queue（主题队列轮转）" `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2)

$task2 = Get-ScheduledTask -TaskName "AI-Berkshire-Industry-Monthly"
$task2.Triggers = @(New-ScheduledTaskTrigger -Monthly -DaysOfMonth 1 -At $RunAt)
Set-ScheduledTask -TaskName "AI-Berkshire-Industry-Monthly" -Trigger $task2.Triggers | Out-Null
Write-Host "   触发：每月 1 号 $RunAt"

Write-Host ""
Write-Host "📋 验证："
Write-Host "  schtasks /query /tn `"AI-Berkshire-*`" /v"
Write-Host ""
Write-Host "🧪 立即触发测试："
Write-Host "  schtasks /run /tn `"AI-Berkshire-Portfolio-Weekly`""
Write-Host ""
Write-Host "🗑️  卸载："
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/uninstall-windows-tasks.ps1"
