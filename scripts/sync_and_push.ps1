# Navigate to the scripts directory
Set-Location -Path "C:\Projects\Gateway_Final\scripts"

# Run the Python sync script
python radioworld_sync.py

# Write an event to log
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Output "[$timestamp] Sync script executed." | Out-File -Append "sync_task.log"

# Navigate back to root to commit and push the updated JSON
Set-Location -Path "C:\Projects\Gateway_Final"

# Add the specific files to Git
git add scripts/live_inventory.json
git add scripts/scraper.log

# Check if there are changes to commit
$gitStatus = git status --porcelain
if ($gitStatus) {
    git commit -m "Automated Hostinger update: Live Inventory Sync"
    git push origin main
    Write-Output "[$timestamp] Changes committed and pushed to GitHub." | Out-File -Append "scripts\sync_task.log"
} else {
    Write-Output "[$timestamp] No inventory changes detected. Skipping push." | Out-File -Append "scripts\sync_task.log"
}
