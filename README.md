# Google Maps Place Scraper

A tool to scrape and organize saved places from Google Maps.

## Progress (March 18, 2024)

✅ Successfully implemented:

- Basic project structure with Python scraper
- Safari automation using AppleScript
- Navigation to favorites list
- Finding and clicking unique places in the list
- Deduplication of places using Set
- Proper panel closing using back button

🔄 Next steps:

- Need to update selectors for details panel based on `@item_details.html` structure
- Implement filtering of bad saved entries
- Group places by region/country
- Create new lists in Google Maps
- Add places to their respective lists

## Setup

1. Create and activate virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Scraper

1. Open Safari and log into Google Maps
2. Navigate to any Google Maps page
3. Run the test script:
   ```bash
   python3 src/test_scraper.py
   ```

## Implementation Notes

### Current Scraping Flow

1. Navigate to favorites list
2. Find all unique places using `.m6QErb` container and `.fontHeadlineSmall` for names
3. Click each unique place using `.SMP2wb.fHEb6e` button
4. Extract details from panel (selectors to be updated based on `@item_details.html`)
5. Close panel using back button
6. Continue to next place

### Debugging Tips

- Console logs are added throughout JavaScript execution
- Python prints progress and any errors
- Check Safari's Web Inspector for element structure

### Known Working Elements

From `local/sample_list_item.html`:

```html
<div class="m6QErb XiKgde">
  <button class="SMP2wb fHEb6e">
    <div class="fontHeadlineSmall">Place Name</div>
    ...
  </button>
</div>
```

## Git Checkpoints

Latest working commits:

1. Successfully clicking into places using correct button selectors
2. Successfully detecting and clicking unique places using Set
3. Improved details panel handling using back button

## Tomorrow's Tasks

1. Get `@item_details.html` structure
2. Update selectors for extracting place details
3. Implement data validation and filtering
4. Begin work on place categorization

## Notes

- Safari must be logged into Google Maps
- Keep Safari as the frontmost window while scraping
- Each place takes about 7 seconds to process (5s load + 2s close)
