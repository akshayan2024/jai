#!/bin/bash
# Script to download Swiss Ephemeris data files

# Create ephemeris directory if it doesn't exist
mkdir -p ephemeris

# Download Swiss Ephemeris data files
echo "Downloading Swiss Ephemeris data files..."

# Main ephemeris files
wget -q -O ephemeris/sepl_18.se1 https://www.astro.com/ftp/swisseph/ephe/sepl_18.se1
wget -q -O ephemeris/seplm18.se1 https://www.astro.com/ftp/swisseph/ephe/seplm18.se1
wget -q -O ephemeris/sepl_24.se1 https://www.astro.com/ftp/swisseph/ephe/sepl_24.se1
wget -q -O ephemeris/seplm24.se1 https://www.astro.com/ftp/swisseph/ephe/seplm24.se1

# Fixed stars and other files
wget -q -O ephemeris/fixstars.cat https://www.astro.com/ftp/swisseph/ephe/fixstars.cat
wget -q -O ephemeris/seas_18.se1 https://www.astro.com/ftp/swisseph/ephe/seas_18.se1
wget -q -O ephemeris/semo_18.se1 https://www.astro.com/ftp/swisseph/ephe/semo_18.se1

# Asteroid files 
wget -q -O ephemeris/seasnam.txt https://www.astro.com/ftp/swisseph/ephe/seasnam.txt
wget -q -O ephemeris/sefstars.txt https://www.astro.com/ftp/swisseph/ephe/sefstars.txt

echo "Download complete. Files saved to ./ephemeris/"
ls -la ephemeris/

# Make the script executable
chmod +x download_ephemeris.sh 