# Run the FastAPI server
Write-Host "Starting Language Translation API..." -ForegroundColor Cyan
Write-Host "Server will be available at: http://localhost:8001" -ForegroundColor Green
Write-Host "API Documentation: http://localhost:8001/docs" -ForegroundColor Green
Write-Host "`nPress CTRL+C to stop the server`n" -ForegroundColor Yellow

# Activate venv and run
Set-Location "c:\Users\vidya\OneDrive\Desktop\final_project\project"
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --host 0.0.0.0 --port 8001
