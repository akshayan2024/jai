# Swiss Ephemeris Files

This document describes the ephemeris files required for the JAI API to function correctly.

## Required Files

The following files are required in the `/app/ephemeris` directory:

1. Main Ephemeris Files:
   - `sepl.se1` - Main ephemeris file
   - `seplm.se1` - Main ephemeris file (modern)
   - `semo.se1` - Moon ephemeris
   - `seas.se1` - Asteroids ephemeris

2. Fixed Stars Files:
   - `fixstars.cat` - Fixed stars catalog
   - `sefstars.txt` - Fixed star names

3. Asteroid Files:
   - `seasnam.txt` - Asteroid names

## File Sources

These files are automatically downloaded during the Docker build process from the official Swiss Ephemeris website (https://www.astro.com/swisseph/).

## File Validation

The application performs the following validations:

1. Checks if the ephemeris directory exists
2. Verifies that required files are present
3. Tests ephemeris calculations during startup
4. Performs periodic health checks

## Error Handling

If any required files are missing or inaccessible, the application will:

1. Log an error with details about the missing file
2. Raise a RuntimeError during initialization
3. Return a 500 error in the health check endpoint

## Manual Installation

If you need to install the files manually:

1. Download the Swiss Ephemeris package from https://www.astro.com/swisseph/
2. Extract the required files to the `/app/ephemeris` directory
3. Ensure all files have the correct permissions (readable by the application user)

## Troubleshooting

Common issues and solutions:

1. **Missing Files**: Ensure all required files are present in the ephemeris directory
2. **Permission Issues**: Check file permissions (should be readable by the application user)
3. **Corrupted Files**: Re-download the files from the official source
4. **Path Issues**: Verify the EPHEMERIS_PATH environment variable is set correctly

## Support

For issues with the Swiss Ephemeris files:

1. Check the official Swiss Ephemeris documentation
2. Contact the Swiss Ephemeris support team
3. Open an issue in the JAI API repository 