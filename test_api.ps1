# Test the API endpoints
Write-Host "`n=== Testing Language Translation API ===" -ForegroundColor Cyan

# Test 1: Health Check
Write-Host "`n1. Health Check Endpoint:" -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8001/health"
    Write-Host "Response:" -ForegroundColor Green
    $health | ConvertTo-Json
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# Test 2: Root Endpoint
Write-Host "`n2. Root Endpoint (API Info):" -ForegroundColor Yellow
try {
    $root = Invoke-RestMethod -Uri "http://localhost:8001/"
    Write-Host "Response:" -ForegroundColor Green
    $root | ConvertTo-Json -Depth 3
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# Test 3: Translation Endpoint (with API key)
Write-Host "`n3. Translation Endpoint:" -ForegroundColor Yellow
try {
    $headers = @{
        "X-API-Key" = "test-key-123"
        "Content-Type" = "application/json"
    }
    $body = @{
        text = "Hello, how are you?"
        target_lang = "es"
        source_lang = "en"
    } | ConvertTo-Json

    $translation = Invoke-RestMethod -Uri "http://localhost:8001/api/v1/translate" -Method POST -Headers $headers -Body $body
    Write-Host "Response:" -ForegroundColor Green
    $translation | ConvertTo-Json -Depth 3
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# Test 4: Language Detection
Write-Host "`n4. Language Detection Endpoint:" -ForegroundColor Yellow
try {
    $headers = @{
        "X-API-Key" = "test-key-123"
        "Content-Type" = "application/json"
    }
    $body = @{
        text = "Bonjour, comment allez-vous?"
    } | ConvertTo-Json

    $detect = Invoke-RestMethod -Uri "http://localhost:8001/api/v1/detect" -Method POST -Headers $headers -Body $body
    Write-Host "Response:" -ForegroundColor Green
    $detect | ConvertTo-Json
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host "`n=== Testing Complete ===" -ForegroundColor Cyan
