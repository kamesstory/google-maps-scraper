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

    def get_place_details(self, place_name: str) -> Dict:
        """
        Click into a place and get its detailed information.
        
        Args:
            place_name: The name of the place to click
            
        Returns:
            Dict: Place details including name, address, type, etc.
        """
        print(f"\nAttempting to click place: {place_name}")
        
        command = f"""
        tell application "Safari"
            tell window 1
                tell current tab
                    -- Click the button using the exact structure from the sample HTML
                    do JavaScript "(() => {{
                        console.log('Looking for place:', '{place_name}');
                        const buttons = Array.from(document.querySelectorAll('.SMP2wb.fHEb6e'));
                        console.log('Found buttons:', buttons.length);
                        
                        for (const button of buttons) {{
                            const nameEl = button.querySelector('.fontHeadlineSmall');
                            if (nameEl) {{
                                const name = nameEl.textContent.trim();
                                console.log('Checking button:', name);
                                if (name === '{place_name}') {{
                                    console.log('Found matching button, clicking...');
                                    button.click();
                                    return true;
                                }}
                            }}
                        }}
                        console.log('No matching button found');
                        return false;
                    }})();"
                    
                    -- Wait longer for details to load
                    delay 5
                    
                    -- Get detailed information
                    set details to do JavaScript "(() => {{
                        console.log('Getting place details...');
                        const nameEl = document.querySelector('h1');
                        const addressEl = document.querySelector('button[data-item-id*=\\"address\\"]');
                        const typeEl = document.querySelector('button[data-item-id*=\\"authority\\"]');
                        const website = document.querySelector('a[data-item-id*=\\"authority\\"]');
                        const phoneEl = document.querySelector('button[data-item-id*=\\"phone\\"]');
                        const ratingEl = document.querySelector('.MW4etd');
                        const reviewCountEl = document.querySelector('.UY7F9');
                        const imageEl = document.querySelector('button[jsaction*=\\"pane.heroHeaderImage\\"] img');
                        
                        const details = {{
                            name: nameEl ? nameEl.textContent.trim() : '',
                            address: addressEl ? addressEl.textContent.trim() : '',
                            type: typeEl ? typeEl.textContent.trim() : '',
                            website: website ? website.href : '',
                            phone: phoneEl ? phoneEl.textContent.trim() : '',
                            rating: ratingEl ? ratingEl.textContent.trim() : '',
                            reviewCount: reviewCountEl ? reviewCountEl.textContent.replace(/[()]/g, '').trim() : '',
                            imageUrl: imageEl ? imageEl.src : ''
                        }};
                        console.log('Place details:', details);
                        return JSON.stringify(details);
                    }})();"
                    
                    -- Click the back button to close the details panel
                    do JavaScript "(() => {{
                        const backButton = document.querySelector('button[jsaction*=\\"pane.back\\"]');
                        if (backButton) {{
                            backButton.click();
                            return true;
                        }}
                        return false;
                    }})();"
                    
                    delay 2
                    
                    return details
                end tell
            end tell
        end tell
        """
        
        try:
            result = self.safari.execute_applescript(command)
            print(f"JavaScript execution result: {result}")
            if result:
                return json.loads(result)
        except Exception as e:
            print(f"Error getting place details: {e}")
            return {}
            
        return {}

    def get_saved_places(self) -> List[Dict]:
        """
        Scrape saved places from the favorites list.
        
        Returns:
            List[Dict]: List of saved places with their details
        """
        places = []
        clicked_names = set()  # Track which places we've already clicked
        
        # Navigate to the favorites list
        if not self.navigate_to_favorites():
            print("Failed to navigate to favorites")
            return places
            
        # Get all place items in the list
        print("Scraping places...")
        command = """
        tell application "Safari"
            tell window 1
                tell current tab
                    set result to do JavaScript "
                        const items = document.querySelectorAll('.m6QErb');
                        console.log('Found ' + items.length + ' items');
                        const seen = new Set();
                        const places = Array.from(items).map(item => {
                            const nameEl = item.querySelector('.fontHeadlineSmall');
                            if (!nameEl) return null;
                            const name = nameEl.textContent.trim();
                            if (seen.has(name)) return null;
                            seen.add(name);
                            return {
                                name: name
                            };
                        }).filter(place => place !== null);
                        console.log('Found unique places:', places);
                        JSON.stringify(places);
                    "
                    return result
                end tell
            end tell
        end tell
        """
        
        try:
            result = self.safari.execute_applescript(command)
            print(f"Raw result from JavaScript: {result}")
            if result:
                place_list = json.loads(result)
                print(f"Found {len(place_list)} unique places")
                
                # Get details for each place
                for i, place in enumerate(place_list):
                    place_name = place.get('name', '').strip()
                    if not place_name or place_name in clicked_names:
                        print(f"Skipping place {i+1}: already clicked or invalid name")
                        continue
                        
                    print(f"\nGetting details for place {i+1}/{len(place_list)}: {place_name}")
                    details = self.get_place_details(place_name)
                    if details:
                        places.append(details)
                        clicked_names.add(place_name)  # Mark this place as clicked
                    else:
                        print(f"Failed to get details for {place_name}")
                        
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