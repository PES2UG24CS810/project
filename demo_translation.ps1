# Demo script to show the current translation behavior
Write-Host "`n=== Language Translation API - Demo ===" -ForegroundColor Cyan
Write-Host "Note: This uses MOCK translations (for testing purposes)" -ForegroundColor Yellow
Write-Host "In production, this would integrate with Google Translate/DeepL/etc.`n" -ForegroundColor Yellow

$apiKey = "test-key-123"
$baseUrl = "http://localhost:8001/api/v1"

# Test 1: English to French
Write-Host "Test 1: Translating 'Hello, how are you?' from English to French" -ForegroundColor Green
$headers = @{
    "X-API-Key" = $apiKey
    "Content-Type" = "application/json"
}
$body = @{
    text = "Hello, how are you?"
    source_lang = "en"
    target_lang = "fr"
} | ConvertTo-Json

try {
    $result = Invoke-RestMethod -Uri "$baseUrl/translate" -Method POST -Headers $headers -Body $body
    Write-Host "Original: $($result.original_text)" -ForegroundColor White
    Write-Host "Translated: $($result.translated_text)" -ForegroundColor Cyan
    Write-Host "From: $($result.source_language) -> To: $($result.target_language)`n" -ForegroundColor Gray
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# Test 2: Spanish to English
Write-Host "Test 2: Translating 'Hola amigo' from Spanish to English" -ForegroundColor Green
$body = @{
    text = "Hola amigo"
    source_lang = "es"
    target_lang = "en"
} | ConvertTo-Json

try {
    $result = Invoke-RestMethod -Uri "$baseUrl/translate" -Method POST -Headers $headers -Body $body
    Write-Host "Original: $($result.original_text)" -ForegroundColor White
    Write-Host "Translated: $($result.translated_text)" -ForegroundColor Cyan
    Write-Host "From: $($result.source_language) -> To: $($result.target_language)`n" -ForegroundColor Gray
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# Test 3: Auto-detect language
Write-Host "Test 3: Auto-detecting language of 'Bonjour le monde'" -ForegroundColor Green
$body = @{
    text = "Bonjour le monde"
    target_lang = "en"
} | ConvertTo-Json

try {
    $result = Invoke-RestMethod -Uri "$baseUrl/translate" -Method POST -Headers $headers -Body $body
    Write-Host "Original: $($result.original_text)" -ForegroundColor White
    Write-Host "Translated: $($result.translated_text)" -ForegroundColor Cyan
    Write-Host "Detected: $($result.source_language) -> To: $($result.target_language)`n" -ForegroundColor Gray
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host "=== Current Limitation ===" -ForegroundColor Yellow
Write-Host "The translator is a MOCK implementation (shows '[Translated to XX]: text')" -ForegroundColor Yellow
Write-Host "To get real translations, you need to integrate an API like:" -ForegroundColor White
Write-Host "  - Google Cloud Translation API" -ForegroundColor Gray
Write-Host "  - Microsoft Translator" -ForegroundColor Gray
Write-Host "  - DeepL API" -ForegroundColor Gray
Write-Host "  - AWS Translate`n" -ForegroundColor Gray
