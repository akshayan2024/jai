$serverProcess = Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "test_server:app", "--host", "0.0.0.0", "--port", "8000" -PassThru -NoNewWindow

# Wait for server to start
Start-Sleep -Seconds 3

Write-Host "Testing all astrological entities..." -ForegroundColor Cyan

try {
    # 1. Test health check
    Write-Host "`nHealth Check:" -ForegroundColor Green
    $response = Invoke-RestMethod -Uri "http://localhost:8000/v1/api/health" -Method Get
    $response | ConvertTo-Json

    # 2. Test root endpoint
    Write-Host "`nRoot Endpoint:" -ForegroundColor Green
    $response = Invoke-RestMethod -Uri "http://localhost:8000/" -Method Get
    $response | ConvertTo-Json

    # Chennai birth data
    $birthData = @{
        birth_date = "1988-12-01"
        birth_time = "21:47:00"
        latitude = 13.0827
        longitude = 80.2707
        timezone_offset = 5.5
        ayanamsa = "lahiri"
    }
    $jsonBody = $birthData | ConvertTo-Json

    # 3. Test basic horoscope (v1/api path)
    Write-Host "`nBasic Horoscope (v1/api path):" -ForegroundColor Green
    $response = Invoke-RestMethod -Uri "http://localhost:8000/v1/api/horoscope" -Method Post -Body $jsonBody -ContentType "application/json"
    Write-Host "Ascendant:" -ForegroundColor Yellow
    $response.ascendant | ConvertTo-Json
    Write-Host "Planets:" -ForegroundColor Yellow
    $response.planets | ConvertTo-Json

    # 4. Test basic horoscope (api/v1 path)
    Write-Host "`nBasic Horoscope (api/v1 path):" -ForegroundColor Green
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/horoscope" -Method Post -Body $jsonBody -ContentType "application/json"
    Write-Host "Status: OK" -ForegroundColor Yellow

    # 5. Test divisional charts
    Write-Host "`nDivisional Charts:" -ForegroundColor Green
    $response = Invoke-RestMethod -Uri "http://localhost:8000/v1/api/horoscope/divisional" -Method Post -Body $jsonBody -ContentType "application/json"
    Write-Host "Navamsa (D-9):" -ForegroundColor Yellow
    $response.navamsa | ConvertTo-Json
    Write-Host "Dasamsa (D-10):" -ForegroundColor Yellow
    $response.dasamsa | ConvertTo-Json

    # 6. Test all divisional charts
    Write-Host "`nAll Divisional Charts:" -ForegroundColor Green
    $response = Invoke-RestMethod -Uri "http://localhost:8000/v1/api/horoscope/divisional/all" -Method Post -Body $jsonBody -ContentType "application/json"
    Write-Host "Available charts: $($response.PSObject.Properties.Name -join ', ')" -ForegroundColor Yellow

    # 7. Test yogas
    Write-Host "`nYogas (Combinations):" -ForegroundColor Green
    $response = Invoke-RestMethod -Uri "http://localhost:8000/v1/api/horoscope/yogas" -Method Post -Body $jsonBody -ContentType "application/json"
    $response.yogas | ConvertTo-Json

    # 8. Test all yogas
    Write-Host "`nAll Yogas:" -ForegroundColor Green
    $response = Invoke-RestMethod -Uri "http://localhost:8000/v1/api/horoscope/yogas/all" -Method Post -Body $jsonBody -ContentType "application/json"
    $response.yogas | ConvertTo-Json

    # 9. Test house positions
    Write-Host "`nHouse Positions:" -ForegroundColor Green
    $response = Invoke-RestMethod -Uri "http://localhost:8000/v1/api/horoscope/houses" -Method Post -Body $jsonBody -ContentType "application/json"
    Write-Host "Houses:" -ForegroundColor Yellow
    $response.houses | ConvertTo-Json
    Write-Host "Aspects:" -ForegroundColor Yellow
    $response.aspects | ConvertTo-Json

    # 10. Test all house positions
    Write-Host "`nAll House Positions:" -ForegroundColor Green
    $response = Invoke-RestMethod -Uri "http://localhost:8000/v1/api/horoscope/houses/all" -Method Post -Body $jsonBody -ContentType "application/json"
    Write-Host "Houses:" -ForegroundColor Yellow
    $response.houses | ConvertTo-Json
    Write-Host "Special Aspects:" -ForegroundColor Yellow
    $response.special_aspects | ConvertTo-Json

    # 11. Test dasha periods
    Write-Host "`nDasha Periods:" -ForegroundColor Green
    $response = Invoke-RestMethod -Uri "http://localhost:8000/v1/api/horoscope/dasha" -Method Post -Body $jsonBody -ContentType "application/json"
    Write-Host "Mahadasha:" -ForegroundColor Yellow
    $response.mahadasha | Select-Object -First 3 | ConvertTo-Json
    Write-Host "Antardasha:" -ForegroundColor Yellow
    $response.antardasha | Select-Object -First 1 | ConvertTo-Json

    # 12. Test all dasha periods
    Write-Host "`nAll Dasha Periods:" -ForegroundColor Green
    $response = Invoke-RestMethod -Uri "http://localhost:8000/v1/api/horoscope/dasha/all" -Method Post -Body $jsonBody -ContentType "application/json"
    Write-Host "Available dasha types: $($response.PSObject.Properties.Name -join ', ')" -ForegroundColor Yellow
    Write-Host "Pratyantardasha sample:" -ForegroundColor Yellow
    $response.pratyantardasha | Select-Object -First 1 | ConvertTo-Json -Depth 3

    # 13. Test transits
    Write-Host "`nTransits:" -ForegroundColor Green
    $transitData = $birthData.Clone()
    $transitData.Add("transit_date", (Get-Date).ToString("yyyy-MM-dd"))
    $jsonTransitBody = $transitData | ConvertTo-Json
    $response = Invoke-RestMethod -Uri "http://localhost:8000/v1/api/horoscope/transits" -Method Post -Body $jsonTransitBody -ContentType "application/json"
    Write-Host "Transit Positions:" -ForegroundColor Yellow
    $response.transits | ConvertTo-Json

    # 14. Test all transits
    Write-Host "`nAll Transits:" -ForegroundColor Green
    $response = Invoke-RestMethod -Uri "http://localhost:8000/v1/api/horoscope/transits/all" -Method Post -Body $jsonTransitBody -ContentType "application/json"
    Write-Host "Available transit data: $($response.PSObject.Properties.Name -join ', ')" -ForegroundColor Yellow
    Write-Host "Special Transits:" -ForegroundColor Yellow
    $response.special_transits | ConvertTo-Json

    Write-Host "`nAll tests completed successfully!" -ForegroundColor Green
}
catch {
    Write-Host "Error occurred: $_" -ForegroundColor Red
}
finally {
    # Stop the server process
    if ($serverProcess -ne $null) {
        Stop-Process -Id $serverProcess.Id -Force
        Write-Host "Server stopped" -ForegroundColor Cyan
    }
} 