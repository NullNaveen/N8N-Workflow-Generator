Write-Host "========================================" -ForegroundColor Cyan
Write-Host "KAGGLE KERNEL STATUS CHECK" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check kernel status
Write-Host "[1] Kernel Status:" -ForegroundColor Yellow
$status = kaggle kernels status navimars/trainer 2>&1
Write-Host "    $status"
Write-Host ""

# Check if it's been running too long
Write-Host "[2] Last Run Time:" -ForegroundColor Yellow
$kernelList = kaggle kernels list --user navimars 2>&1 | Select-String "trainer"
Write-Host "    $kernelList"
Write-Host ""

# Try to get output files
Write-Host "[3] Attempting to list output files..." -ForegroundColor Yellow
$outputAttempt = kaggle kernels output navimars/trainer -p "$env:TEMP\kaggle_check" 2>&1
if (Test-Path "$env:TEMP\kaggle_check") {
    $files = Get-ChildItem "$env:TEMP\kaggle_check" -Recurse
    if ($files.Count -gt 0) {
        Write-Host "    SUCCESS! Found $($files.Count) output files:" -ForegroundColor Green
        $files | ForEach-Object { Write-Host "    - $($_.Name)" -ForegroundColor Green }
    } else {
        Write-Host "    No output files available yet" -ForegroundColor Yellow
    }
    Remove-Item "$env:TEMP\kaggle_check" -Recurse -Force -ErrorAction SilentlyContinue
} else {
    Write-Host "    $outputAttempt" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "WHAT TO DO:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to: https://www.kaggle.com/code/navimars/trainer" -ForegroundColor White
Write-Host "2. Check the console output at the bottom" -ForegroundColor White
Write-Host "3. Look for:" -ForegroundColor White
Write-Host "   - 'TRAINING COMPLETED' = Done!" -ForegroundColor Green
Write-Host "   - Progress bars/steps = Still running" -ForegroundColor Yellow
Write-Host "   - Error messages = Failed" -ForegroundColor Red
Write-Host ""
