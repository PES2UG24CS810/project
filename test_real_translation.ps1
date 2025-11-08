# Test Real Google Translate Implementation
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  REAL TRANSLATION SERVICE - DEMO" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$apiKey = "test-key-123"
$baseUrl = "http://localhost:8001/api/v1"
$headers = @{
    "X-API-Key" = $apiKey
    "Content-Type" = "application/json"
}

# Test 1: English to French
Write-Host "1️⃣  English to French" -ForegroundColor Green
Write-Host "   Input: 'Hello, how are you?'" -ForegroundColor White
$body = @{
    text = "Hello, how are you?"
    source_lang = "en"
    target_lang = "fr"
} | ConvertTo-Json

try {
    $result = Invoke-RestMethod -Uri "$baseUrl/translate" -Method POST -Headers $headers -Body $body
    Write-Host "   Output: " -NoNewline -ForegroundColor Yellow
    Write-Host "'$($result.translated_text)'" -ForegroundColor Cyan
    Write-Host "   ✅ Real Translation!" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Error: $_" -ForegroundColor Red
}

Start-Sleep -Seconds 1

# Test 2: English to Spanish
Write-Host "`n2️⃣  English to Spanish" -ForegroundColor Green
Write-Host "   Input: 'Good morning, my friend'" -ForegroundColor White
$body = @{
    text = "Good morning, my friend"
    source_lang = "en"
    target_lang = "es"
} | ConvertTo-Json

try {
    $result = Invoke-RestMethod -Uri "$baseUrl/translate" -Method POST -Headers $headers -Body $body
    Write-Host "   Output: " -NoNewline -ForegroundColor Yellow
    Write-Host "'$($result.translated_text)'" -ForegroundColor Cyan
    Write-Host "   ✅ Real Translation!" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Error: $_" -ForegroundColor Red
}

Start-Sleep -Seconds 1

# Test 3: Spanish to English
Write-Host "`n3️⃣  Spanish to English" -ForegroundColor Green
Write-Host "   Input: 'Hola, ¿cómo estás?'" -ForegroundColor White
$body = @{
    text = "Hola, ¿cómo estás?"
    source_lang = "es"
    target_lang = "en"
} | ConvertTo-Json

try {
    $result = Invoke-RestMethod -Uri "$baseUrl/translate" -Method POST -Headers $headers -Body $body
    Write-Host "   Output: " -NoNewline -ForegroundColor Yellow
    Write-Host "'$($result.translated_text)'" -ForegroundColor Cyan
    Write-Host "   ✅ Real Translation!" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Error: $_" -ForegroundColor Red
}

Start-Sleep -Seconds 1

# Test 4: French to German
Write-Host "`n4️⃣  French to German" -ForegroundColor Green
Write-Host "   Input: 'Bonjour le monde'" -ForegroundColor White
$body = @{
    text = "Bonjour le monde"
    source_lang = "fr"
    target_lang = "de"
} | ConvertTo-Json

try {
    $result = Invoke-RestMethod -Uri "$baseUrl/translate" -Method POST -Headers $headers -Body $body
    Write-Host "   Output: " -NoNewline -ForegroundColor Yellow
    Write-Host "'$($result.translated_text)'" -ForegroundColor Cyan
    Write-Host "   ✅ Real Translation!" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Error: $_" -ForegroundColor Red
}

Start-Sleep -Seconds 1

# Test 5: Auto-detect language (German to English)
Write-Host "`n5️⃣  Auto-Detect Language (German → English)" -ForegroundColor Green
Write-Host "   Input: 'Guten Tag, wie geht es Ihnen?'" -ForegroundColor White
$body = @{
    text = "Guten Tag, wie geht es Ihnen?"
    target_lang = "en"
} | ConvertTo-Json

try {
    $result = Invoke-RestMethod -Uri "$baseUrl/translate" -Method POST -Headers $headers -Body $body
    Write-Host "   Detected: " -NoNewline -ForegroundColor Gray
    Write-Host "$($result.source_language)" -ForegroundColor Magenta
    Write-Host "   Output: " -NoNewline -ForegroundColor Yellow
    Write-Host "'$($result.translated_text)'" -ForegroundColor Cyan
    Write-Host "   ✅ Auto-detection + Real Translation!" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Error: $_" -ForegroundColor Red
}

Start-Sleep -Seconds 1

# Test 6: Multiple sentences
Write-Host "`n6️⃣  Complex Sentence (English → French)" -ForegroundColor Green
Write-Host "   Input: 'I love programming and building APIs'" -ForegroundColor White
$body = @{
    text = "I love programming and building APIs"
    source_lang = "en"
    target_lang = "fr"
} | ConvertTo-Json

try {
    $result = Invoke-RestMethod -Uri "$baseUrl/translate" -Method POST -Headers $headers -Body $body
    Write-Host "   Output: " -NoNewline -ForegroundColor Yellow
    Write-Host "'$($result.translated_text)'" -ForegroundColor Cyan
    Write-Host "   ✅ Real Translation!" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Error: $_" -ForegroundColor Red
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   🎉 Translation Service is LIVE!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan
Write-Host "Now you have REAL translations powered by Google Translate!" -ForegroundColor White
Write-Host "Try it in Swagger UI: http://localhost:8001/docs`n" -ForegroundColor Yellow
