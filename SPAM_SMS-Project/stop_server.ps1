# Stop any running Python processes
$processes = Get-Process python -ErrorAction SilentlyContinue

if ($processes) {
    Write-Host "Stopping Python processes..."
    $processes | ForEach-Object {
        Write-Host "- Stopping process ID $($_.Id) ($($_.ProcessName))"
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
    }
    Write-Host "All Python processes have been stopped."
} else {
    Write-Host "No Python processes are currently running."
}

# If you want to deactivate the virtual environment, uncomment the following lines:
# if (Test-Path ".venv\Scripts\deactivate.ps1") {
#     Write-Host "Deactivating virtual environment..."
#     deactivate
# }
