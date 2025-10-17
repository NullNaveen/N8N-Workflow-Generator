# Script to wait for Kaggle kernel to finish and download outputs

$MaxWaitTime = 600  # 10 minutes
$CheckInterval = 30  # Check every 30 seconds
$ElapsedTime = 0

Write-Host "⏳ Waiting for Kaggle kernel to complete..."
Write-Host "Maximum wait time: 10 minutes`n"

while ($ElapsedTime -lt $MaxWaitTime) {
    $status = kaggle kernels status navimars/trainer 2>&1
    
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Status: $status"
    
    if ($status -match "COMPLETE" -or $status -match "complete") {
        Write-Host "`n✅ Kernel completed!"
        break
    } elseif ($status -match "ERROR" -or $status -match "error") {
        Write-Host "`n❌ Kernel failed!"
        exit 1
    }
    
    $ElapsedTime += $CheckInterval
    Start-Sleep -Seconds $CheckInterval
}

if ($ElapsedTime -ge $MaxWaitTime) {
    Write-Host "`n⏱️ Maximum wait time reached (10 minutes). Attempting download anyway..."
}

Write-Host "`n📥 Downloading kernel outputs..."
kaggle kernels output navimars/trainer -p "c:\Users\Nike\Documents\Programming\Projects\N8N\models"

Write-Host "`n✅ Download complete!"
Write-Host "`n📂 Downloaded files:"
Get-ChildItem -Path "c:\Users\Nike\Documents\Programming\Projects\N8N\models" -Recurse | ForEach-Object {
    $size = if ($_.PSIsContainer) { "-" } else { "[$('{0:N2}' -f ($_.Length/1MB)) MB]" }
    Write-Host "   $($_.FullName.Replace('c:\Users\Nike\Documents\Programming\Projects\N8N\models\', '')) $size"
}
