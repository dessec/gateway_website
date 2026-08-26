param(
    [string]$CommitMessage = "Update website content and assets"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "1. Deploying to Live Namecheap Hosting" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

scp "$PSScriptRoot\index.html" "namecheap-gateway:public_html/index.html"
scp -r "$PSScriptRoot\pages\*" "namecheap-gateway:public_html/pages/"
scp -r "$PSScriptRoot\styles\*" "namecheap-gateway:public_html/styles/"
scp -r "$PSScriptRoot\assets\*" "namecheap-gateway:public_html/assets/"
if (Test-Path "$PSScriptRoot\send_message.php") {
    scp "$PSScriptRoot\send_message.php" "namecheap-gateway:public_html/send_message.php"
}
if (Test-Path "$PSScriptRoot\save-pin.php") {
    scp "$PSScriptRoot\save-pin.php" "namecheap-gateway:public_html/save-pin.php"
}

Write-Host "`n✅ Pushed changes directly to Namecheap (Live)!" -ForegroundColor Green

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "2. Pushing Backup to GitHub Repository" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

cd $PSScriptRoot
git add -A
$status = git status --porcelain
if ($status) {
    git commit -m "$CommitMessage"
    git push origin main
    Write-Host "`n✅ Backup successfully pushed to GitHub (origin main)!" -ForegroundColor Green
} else {
    Write-Host "`nℹ️ GitHub repository is already up to date." -ForegroundColor Cyan
}

Write-Host "`n🎉 All tasks complete: Live Site updated & GitHub Backup saved!" -ForegroundColor Green
