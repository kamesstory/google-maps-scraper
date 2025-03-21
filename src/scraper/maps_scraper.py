"""
Google Maps scraping module for collecting saved places.
"""
from typing import List, Dict, Optional
from datetime import datetime
import time
import json
from pathlib import Path
from .safari_automation import SafariAutomation

class MapsScraper:
    def __init__(self):
        self.safari = SafariAutomation()
        self.base_url = "https://www.google.com/maps"
        # Load the starting link from file
        starting_link_path = Path("local/starting_link.txt")
        if starting_link_path.exists():
            with open(starting_link_path, "r") as f:
                self.starting_url = f.read().strip()
        else:
            print("Error: No starting link found in local/starting_link.txt")
            self.starting_url = None

    def navigate_to_favorites(self) -> bool:
        """
        Navigate to the favorites list URL.
        
        Returns:
            bool: True if navigation was successful
        """
        if not self.starting_url:
            print("Error: No starting URL configured")
            return False
            
        print(f"Navigating to favorites list...")
        if not self.safari.navigate_to_url(self.starting_url):
            print("Failed to navigate to URL")
            return False
            
        # Simple static wait for page to load
        print("Waiting 5 seconds for page to load...")
        time.sleep(5)
            
        # Get the current URL to verify we're on the right page
        current_url = self.safari.get_current_url()
        print(f"Current URL: {current_url}")
            
        return True

    def get_saved_places(self) -> List[Dict]:
        """
        Scrape saved places from the favorites list.
        
        Returns:
            List[Dict]: List of saved places with their details
        """
        places = []
        
        # Navigate to the favorites list
        if not self.navigate_to_favorites():
            print("Failed to navigate to favorites")
            return places
            
        # Get all place items in the list
        print("Scraping places...")
        command = """
        tell application "Safari"
            tell window 1
                set places to do JavaScript "
                    const items = document.querySelectorAll('.m6QErb');
                    console.log('Found ' + items.length + ' items');
                    const places = Array.from(items).map(item => {
                        const nameEl = item.querySelector('.fontHeadlineSmall');
                        const ratingEl = item.querySelector('.MW4etd');
                        const reviewCountEl = item.querySelector('.UY7F9');
                        const priceEl = item.querySelector('.IIrLbb span');
                        const typeEl = item.querySelector('.IIrLbb span:last-child');
                        const imageEl = item.querySelector('.WkIe8');
                        const place = {
                            name: nameEl ? nameEl.textContent : '',
                            rating: ratingEl ? ratingEl.textContent : '',
                            reviewCount: reviewCountEl ? reviewCountEl.textContent.replace(/[()]/g, '') : '',
                            price: priceEl ? priceEl.textContent : '',
                            type: typeEl ? typeEl.textContent.replace('· ', '') : '',
                            imageUrl: imageEl ? imageEl.src : ''
                        };
                        console.log('Scraped place:', place);
                        return place;
                    });
                    console.log('Returning places:', JSON.stringify(places));
                    return JSON.stringify(places);
                " in current tab
                return places
            end tell
        end tell
        """
        
        try:
            result = self.safari.execute_applescript(command)
            print(f"Raw result from JavaScript: {result}")
            if result:
                places = json.loads(result)
                print(f"Found {len(places)} places")
        except Exception as e:
            print(f"Error scraping places: {e}")
            print(f"Result that caused error: {result}")
            
        return places

    def save_places_to_file(self, places: List[Dict], filename: Optional[str] = None) -> bool:
        """
        Save scraped places to a JSON file.
        
        Args:
            places: List of place dictionaries
            filename: Optional custom filename
            
        Returns:
            bool: True if save was successful
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"outputs/places_{timestamp}.json"
            
        try:
            with open(filename, "w") as f:
                json.dump(places, f, indent=2)
            print(f"Saved places to {filename}")
            return True
        except Exception as e:
            print(f"Error saving places: {e}")
            return False 