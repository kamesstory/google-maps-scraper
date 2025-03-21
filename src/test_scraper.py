"""
Test script for basic scraping functionality.
"""
from scraper.maps_scraper import MapsScraper

def main():
    print("Starting Google Maps scraper test...")
    
    # Initialize scraper
    scraper = MapsScraper()
    
    # Try to get saved places
    print("\nAttempting to scrape saved places...")
    places = scraper.get_saved_places()
    
    print(f"\nFound {len(places)} places")
    
    # Save results
    if places:
        scraper.save_places_to_file(places)
    else:
        print("No places found to save")

if __name__ == "__main__":
    main() 