# Sync latest files down from Namecheap to local directory
$backupDir = Join-Path $PSScriptRoot "_backups\backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
Write-Host "Creating safety backup in $backupDir..." -ForegroundColor Cyan

# Backup current local html/pages
if (Test-Path (Join-Path $PSScriptRoot "index.html")) { Copy-Item (Join-Path $PSScriptRoot "index.html") $backupDir -Force }
if (Test-Path (Join-Path $PSScriptRoot "pages")) { Copy-Item -Recurse (Join-Path $PSScriptRoot "pages") $backupDir -Force }
if (Test-Path (Join-Path $PSScriptRoot "styles")) { Copy-Item -Recurse (Join-Path $PSScriptRoot "styles") $backupDir -Force }

Write-Host "Pulling latest files from Namecheap (public_html)..." -ForegroundColor Yellow
scp -r "namecheap-gateway:public_html/index.html" "$PSScriptRoot\"
scp -r "namecheap-gateway:public_html/pages" "$PSScriptRoot\"
scp -r "namecheap-gateway:public_html/styles" "$PSScriptRoot\"
scp -r "namecheap-gateway:public_html/assets" "$PSScriptRoot\"
scp -r "namecheap-gateway:public_html/live_inventory.json" "$PSScriptRoot\"
scp -r "namecheap-gateway:public_html/send_message.php" "$PSScriptRoot\"
scp -r "namecheap-gateway:public_html/save-pin.php" "$PSScriptRoot\"
if (Test-Path (Join-Path $PSScriptRoot "scrape_radioworld_inventory.py")) {
    scp "namecheap-gateway:public_html/scrape_radioworld_inventory.py" "$PSScriptRoot\"
}

Write-Host "`n✅ Successfully synced down latest live site from Namecheap!" -ForegroundColor Green
