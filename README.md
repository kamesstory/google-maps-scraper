# Google Maps Saved Places Scraper

This script automates the process of scraping your saved places from Google Maps and saves them to a CSV file with detailed information about each place.

## Features

- Automated Google Maps login
- Scrapes all saved places (including custom saved places)
- Extracts detailed information including:
  - Place name
  - Address
  - Phone number
  - Website
  - Rating
  - Number of reviews
  - Category
  - Description
  - Opening hours
  - Timestamp of scraping

## Prerequisites

- Python 3.7 or higher
- Chrome browser installed
- Google account with saved places in Google Maps

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:

   ```bash
   python google_maps_scraper.py
   ```

2. When prompted, complete the Google Maps login process in the browser window that opens
3. Press Enter in the terminal once you've successfully logged in
4. The script will automatically:
   - Navigate to your saved places
   - Extract information for each place
   - Save the results to a CSV file named `google_maps_saved_places_YYYYMMDD_HHMMSS.csv`

## Notes

- The script includes a small delay between processing places to avoid rate limiting
- If you encounter any issues with the browser window, you can uncomment the headless mode option in the script
- The script will automatically handle cases where certain information is not available for a place

## Troubleshooting

If you encounter any issues:

1. Make sure you have the latest version of Chrome installed
2. Check that all dependencies are installed correctly
3. Ensure you have a stable internet connection
4. Try running the script without headless mode if you experience any issues
