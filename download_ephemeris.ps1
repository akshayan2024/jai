# PowerShell script to download and extract Swiss Ephemeris data files

# Create ephemeris directory if it doesn't exist
New-Item -ItemType Directory -Force -Path "ephemeris"

# Download Swiss Ephemeris package
Write-Host "Downloading Swiss Ephemeris package..."
$url = "https://www.astro.com/swisseph/swisseph.zip"
$zipFile = "swisseph.zip"

try {
    Invoke-WebRequest -Uri $url -OutFile $zipFile
    Write-Host "Successfully downloaded Swiss Ephemeris package"
} catch {
    Write-Host "Failed to download Swiss Ephemeris package. Please download it manually from https://www.astro.com/swisseph/swisseph.zip"
    exit 1
}

# Extract the zip file
Write-Host "Extracting Swiss Ephemeris files..."
try {
    Expand-Archive -Path $zipFile -DestinationPath "temp_ephemeris" -Force
    Write-Host "Successfully extracted files"
} catch {
    Write-Host "Failed to extract files. Please extract the zip file manually and copy the required files to the ephemeris directory."
    exit 1
}

# Copy required files to ephemeris directory
Write-Host "Copying required files to ephemeris directory..."
$requiredFiles = @(
    "sepl.se1",      # Main ephemeris file
    "seplm.se1",     # Main ephemeris file (modern)
    "seas.se1",      # Asteroids ephemeris
    "semo.se1",      # Moon ephemeris
    "fixstars.cat",  # Fixed stars catalog
    "seasnam.txt",   # Asteroid names
    "sefstars.txt"   # Fixed star names
)

foreach ($file in $requiredFiles) {
    $sourcePath = Join-Path "temp_ephemeris" $file
    $destPath = Join-Path "ephemeris" $file
    if (Test-Path $sourcePath) {
        Copy-Item -Path $sourcePath -Destination $destPath -Force
        Write-Host "Copied $file"
    } else {
        Write-Host "Warning: $file not found in the package"
    }
}

# Clean up
Write-Host "Cleaning up temporary files..."
Remove-Item -Path $zipFile -Force
Remove-Item -Path "temp_ephemeris" -Recurse -Force

Write-Host "`nDownload and setup complete. Files saved to ./ephemeris/"
Get-ChildItem -Path "ephemeris" 