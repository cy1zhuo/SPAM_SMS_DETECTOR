# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python version: $pythonVersion"
} catch {
    Write-Error "Python is not installed or not in PATH. Please install Python 3.7 or later and ensure it's added to your system PATH."
    Write-Host "You can download Python from: https://www.python.org/downloads/"
    exit 1
}

# Stop any running Python processes
Write-Host "Stopping any running Python processes..."
Stop-Process -Name "python" -Force -ErrorAction SilentlyContinue

# Set the working directory to the script's directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Check if virtual environment exists, if not create it
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
    if (-not $?) {
        Write-Error "Failed to create virtual environment. Please check your Python installation."
        exit 1
    }
}

# Activate the virtual environment
try {
    Write-Host "Activating virtual environment..."
    .\.venv\Scripts\Activate.ps1
    if (-not $?) {
        throw "Failed to activate virtual environment"
    }
} catch {
    Write-Error "Failed to activate virtual environment: $_"
    exit 1
}

# Install requirements
Write-Host "Installing/verifying dependencies..."
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
if (-not $?) {
    Write-Error "Failed to install dependencies. Please check your internet connection and try again."
    exit 1
}

# Start the Flask server
Write-Host "`nStarting Flask server..."
Write-Host "Server will be available at: http://127.0.0.1:5000"
Write-Host "Press Ctrl+C to stop the server`n"

try {
    # Start the server
    python backend/app.py
} catch {
    Write-Error "Error starting the server: $_"
} finally {
    # Deactivate the virtual environment when done
    Write-Host "`nDeactivating virtual environment..."
    deactivate
}
