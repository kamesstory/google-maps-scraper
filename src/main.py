"""
Main entry point for the Google Maps Saved Places Manager.
"""
import json
from datetime import datetime
from pathlib import Path
from scraper.maps_scraper import MapsScraper
from processor.place_filter import PlaceFilter
from organizer.region_organizer import RegionOrganizer
from automation.list_manager import ListManager

def main():
    # Initialize components
    scraper = MapsScraper()
    filter = PlaceFilter()
    organizer = RegionOrganizer()
    list_manager = ListManager()

    # Create outputs directory if it doesn't exist
    outputs_dir = Path("outputs")
    outputs_dir.mkdir(exist_ok=True)

    # Scrape saved places
    print("Scraping saved places...")
    places = scraper.get_saved_places()
    
    # Save raw data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_file = outputs_dir / f"raw_places_{timestamp}.json"
    with open(raw_file, "w") as f:
        json.dump(places, f, indent=2)
    print(f"Saved raw data to {raw_file}")

    # Filter places
    print("Filtering places...")
    valid_places = filter.filter_places(places)
    
    # Organize by region
    print("Organizing places by region...")
    organized_places = organizer.organize_by_region(valid_places)
    
    # Save organized data
    organized_file = outputs_dir / f"organized_places_{timestamp}.json"
    with open(organized_file, "w") as f:
        json.dump(organized_places, f, indent=2)
    print(f"Saved organized data to {organized_file}")

    # TODO: Implement list creation and population
    # This will be done after testing the scraping and organization

if __name__ == "__main__":
    main() 