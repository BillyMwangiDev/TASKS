Write-Host "Starting TASKY - Task Manager..." -ForegroundColor Green
Write-Host ""
Write-Host "Make sure you have activated your virtual environment if you're using one." -ForegroundColor Yellow
Write-Host ""

try {
    python main.py
} catch {
    Write-Host "Error running the application: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
