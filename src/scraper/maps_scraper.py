"""
Google Maps scraping module for collecting saved places.
"""
from typing import List, Dict, Optional
from datetime import datetime
import time
import json
import yaml
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
        # Initialize output file with current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_file = f"outputs/places_{timestamp}.yaml"
        self.places = []  # Keep track of places in memory
        # Create outputs directory if it doesn't exist
        Path("outputs").mkdir(exist_ok=True)
        # Create empty YAML file immediately with proper format
        with open(self.output_file, "w") as f:
            f.write("places:\n")  # Start with a proper YAML structure
        print(f"Created new YAML file: {self.output_file}")

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
                        const descriptionEl = document.querySelector('.PYvSYb');
                        const hoursEl = document.querySelector('button[data-item-id*=\\"oh\\"]');
                        const priceEl = document.querySelector('button[data-item-id*=\\"price\\"]');
                        
                        const details = {{
                            name: nameEl ? nameEl.textContent.trim() : '',
                            address: addressEl ? addressEl.textContent.trim() : '',
                            type: typeEl ? typeEl.textContent.trim() : '',
                            website: website ? website.href : '',
                            phone: phoneEl ? phoneEl.textContent.trim() : '',
                            rating: ratingEl ? ratingEl.textContent.trim() : '',
                            reviewCount: reviewCountEl ? reviewCountEl.textContent.replace(/[()]/g, '').trim() : '',
                            imageUrl: imageEl ? imageEl.src : '',
                            description: descriptionEl ? descriptionEl.textContent.trim() : '',
                            hours: hoursEl ? hoursEl.textContent.trim() : '',
                            price: priceEl ? priceEl.textContent.trim() : ''
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
            if result and result != "null":
                try:
                    details = json.loads(result)
                    # Only return if we got actual details
                    if details.get('name') and details.get('name') != 'Favorites':
                        print(f"Successfully got details for: {details.get('name')}")
                        return details
                    else:
                        print(f"Invalid details returned for {place_name}")
                except json.JSONDecodeError as e:
                    print(f"Failed to parse JSON result: {e}")
                    print(f"Raw result: {result}")
        except Exception as e:
            print(f"Error getting place details: {e}")
            
        return {}

    def save_place(self, place: Dict) -> bool:
        """
        Save a single place to the output file.
        
        Args:
            place: Place details dictionary
            
        Returns:
            bool: True if save was successful
        """
        try:
            # Append to in-memory list
            self.places.append(place)
            # Write entire list to file
            with open(self.output_file, "w") as f:
                f.write("places:\n")  # Start with proper YAML structure
                for p in self.places:
                    f.write("- ")  # Start each place with a dash
                    yaml.dump(p, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            print(f"Saved place: {place.get('name', 'Unknown')} to {self.output_file}")
            return True
        except Exception as e:
            print(f"Error saving place: {e}")
            return False

    def get_saved_places(self) -> List[Dict]:
        """
        Scrape saved places from the favorites list.
        
        Returns:
            List[Dict]: List of saved places with their details
        """
        clicked_names = set()  # Track which places we've already clicked
        
        # Navigate to the favorites list
        if not self.navigate_to_favorites():
            print("Failed to navigate to favorites")
            return self.places
            
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
                        # Save immediately after getting details
                        if self.save_place(details):
                            clicked_names.add(place_name)  # Only mark as clicked if save was successful
                            print(f"Successfully saved and processed: {place_name}")
                        else:
                            print(f"Failed to save details for {place_name}")
                    else:
                        print(f"Failed to get details for {place_name}")
                        
        except Exception as e:
            print(f"Error scraping places: {e}")
            print(f"Result that caused error: {result}")
            
        return self.places

    def save_places_to_file(self, places: List[Dict], filename: Optional[str] = None) -> bool:
        """
        Save scraped places to a YAML file.
        
        Args:
            places: List of place dictionaries
            filename: Optional custom filename
            
        Returns:
            bool: True if save was successful
        """
        if filename:
            self.output_file = filename
            
        try:
            with open(self.output_file, "w") as f:
                yaml.dump(self.places, f, default_flow_style=False, sort_keys=False)
            print(f"Saved all places to {self.output_file}")
            return True
        except Exception as e:
            print(f"Error saving places: {e}")
            return False 