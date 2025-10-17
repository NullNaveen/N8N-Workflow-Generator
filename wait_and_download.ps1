$attempt = 0
$maxAttempts = 20

while ($attempt -lt $maxAttempts) {
    $attempt++
    $timestamp = Get-Date -Format "HH:mm:ss"
    
    Write-Host "[$timestamp] Attempt $attempt - Checking kernel status..."
    
    $status = kaggle kernels status navimars/trainer 2>&1
    Write-Host "Status: $status"
    
    Write-Host "Attempting to download..."
    kaggle kernels output navimars/trainer -p "c:\Users\Nike\Documents\Programming\Projects\N8N\models" 2>&1 | Out-Null
    
    $files = Get-ChildItem -Path "c:\Users\Nike\Documents\Programming\Projects\N8N\models" -Recurse -ErrorAction SilentlyContinue
    if ($files.Count -gt 0) {
        Write-Host ""
        Write-Host "SUCCESS! Downloaded $($files.Count) files"
        Write-Host ""
        foreach ($file in $files) {
            Write-Host "[OK] $($file.FullName.Replace('c:\Users\Nike\Documents\Programming\Projects\N8N\models\', ''))"
        }
        exit 0
    }
    
    if ($attempt -lt $maxAttempts) {
        Write-Host "No files yet. Waiting 30 seconds..."
        Write-Host ""
        Start-Sleep -Seconds 30
    }
}

Write-Host ""
Write-Host "Max attempts reached. Kernel may still be processing."
Write-Host ""
