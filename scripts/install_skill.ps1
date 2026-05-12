# install_skill.ps1
# 將專案內更新好的 SKILL.md 安裝到 Claude skills 目錄
# 用法：在 PowerShell 執行  .\scripts\install_skill.ps1

$skillSrc = "$PSScriptRoot\..\skills\podcast-summarizer\SKILL.md"
$skillDst = "$env:APPDATA\Claude\local-agent-mode-sessions\skills-plugin"

# 找到 podcast-summarizer 的安裝位置（路徑含動態 session ID，用 Get-ChildItem 搜尋）
$target = Get-ChildItem -Path $skillDst -Recurse -Filter "SKILL.md" |
    Where-Object { $_.FullName -match "podcast-summarizer" } |
    Select-Object -First 1

if (-not $target) {
    Write-Error "找不到 podcast-summarizer skill 安裝位置，請確認 skill 已安裝。"
    exit 1
}

Copy-Item -Path $skillSrc -Destination $target.FullName -Force
Write-Host "✅ 已更新：$($target.FullName)"
