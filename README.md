# Google Maps Saved Places Manager

This project helps manage and organize Google Maps saved places by:

1. Scraping saved places from Google Maps Favorites
2. Filtering out invalid or outdated entries
3. Organizing places into region-based lists
4. Automatically adding places to new Google Maps lists

## Project Structure

- `src/` - Source code directory
  - `scraper/` - Google Maps scraping functionality
  - `processor/` - Data processing and filtering
  - `organizer/` - List organization and management
  - `automation/` - AppleScript automation for browser control
- `outputs/` - Directory for storing scraped data and processed results
- `tests/` - Test files
- `requirements.txt` - Python dependencies

## Setup

1. Create and activate virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix/macOS
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Ensure you're logged into Google Maps in Safari
2. Run the scraper to collect saved places
3. Process and filter the data
4. Create new lists in Google Maps
5. Use the automation script to add places to lists

## Development Status

- [ ] Basic project structure
- [ ] Safari automation setup
- [ ] Google Maps scraping implementation
- [ ] Data processing and filtering
- [ ] List organization
- [ ] Automated list population

## Notes

- This project uses AppleScript for browser automation
- Data is stored locally in the outputs directory
- Regular backups of scraped data are recommended
