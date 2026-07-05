# scripts/uninstall-windows-tasks.ps1
# 卸载 install-windows-tasks.ps1 注册的 2 个任务。
#
# 用法：
#   powershell -ExecutionPolicy Bypass -File scripts/uninstall-windows-tasks.ps1

$ErrorActionPreference = "Continue"  # 单个任务不存在时不中断

$tasks = @(
    "AI-Berkshire-Portfolio-Weekly",
    "AI-Berkshire-Industry-Monthly"
)

foreach ($name in $tasks) {
    $existing = Get-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue
    if ($existing) {
        Unregister-ScheduledTask -TaskName $name -Confirm:$false
        Write-Host "🗑️  已卸载：$name"
    } else {
        Write-Host "ℹ️  未注册（跳过）：$name"
    }
}
