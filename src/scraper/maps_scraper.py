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
            self.starting_url = f"{self.base_url}/saved"

    def navigate_to_saved_places(self) -> bool:
        """
        Navigate to Google Maps saved places page.
        
        Returns:
            bool: True if navigation was successful
        """
        print(f"Navigating to: {self.starting_url}")
        if not self.safari.navigate_to_url(self.starting_url):
            print("Failed to navigate to URL")
            return False
            
        # Wait for page to load
        print("Waiting for page to load...")
        if not self.wait_for_page_load():
            print("Page load timeout")
            return False
            
        # Get the current URL to verify we're on the right page
        current_url = self.safari.get_current_url()
        print(f"Current URL: {current_url}")
        
        # Skip login check since we're always logged in
        # print("Checking login state...")
        # if not self.safari.check_login_state():
        #     print("Error: Not logged into Google Maps. Please ensure you're logged in with jhw513@gmail.com")
        #     return False
            
        return True

    def wait_for_page_load(self, timeout: int = 10) -> bool:
        """
        Wait for the page to load using AppleScript.
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            bool: True if page loaded successfully
        """
        command = """
        tell application "Safari"
            tell window 1
                repeat until (do JavaScript "document.readyState === 'complete'" in current tab) is "true"
                    delay 0.5
                end repeat
                return true
            end tell
        end tell
        """
        try:
            self.safari.execute_applescript(command)
            # Add a small delay to ensure dynamic content starts loading
            time.sleep(1)
            return True
        except Exception as e:
            print(f"Error waiting for page load: {e}")
            return False

    def get_saved_places(self) -> List[Dict]:
        """
        Scrape saved places from Google Maps.
        
        Returns:
            List[Dict]: List of saved places with their details
        """
        places = []
        
        # Navigate to the page
        if not self.navigate_to_saved_places():
            print("Failed to navigate to saved places")
            return places
            
        # Get the current URL to verify we're on the right page
        current_url = self.safari.get_current_url()
        print(f"Current URL: {current_url}")
        
        # Wait for favorites section to load
        print("Waiting for favorites section...")
        if not self.safari.wait_for_element('div[aria-label="Favorites"]'):
            print("Warning: Favorites section not found")
            return places
            
        # Get all place items in the favorites section
        print("Scraping favorites...")
        command = """
        tell application "Safari"
            tell window 1
                set places to do JavaScript "
                    Array.from(document.querySelectorAll('div[aria-label=\\"Favorites\\"] div[role=\\"listitem\\"]')).map(item => {
                        const nameEl = item.querySelector('div[role=\\"heading\\"]');
                        const addressEl = item.querySelector('div[role=\\"button\\"]');
                        return {
                            name: nameEl ? nameEl.textContent : '',
                            address: addressEl ? addressEl.textContent : '',
                            url: item.querySelector('a') ? item.querySelector('a').href : ''
                        };
                    });
                " in current tab
                return places
            end tell
        end tell
        """
        
        try:
            result = self.safari.execute_applescript(command)
            if result:
                places = json.loads(result)
                print(f"Found {len(places)} places in favorites")
        except Exception as e:
            print(f"Error scraping places: {e}")
            
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