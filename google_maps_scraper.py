from selenium import webdriver
from selenium.webdriver.safari.service import Service
from selenium.webdriver.safari.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time
import json
from datetime import datetime
import os
import sys
import platform
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoogleMapsScraper:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.places = []
        
    def setup_driver(self):
        """Set up the Safari WebDriver with appropriate options."""
        try:
            logger.info("Setting up Safari WebDriver...")
            options = Options()
            
            logger.info("Initializing Safari WebDriver...")
            self.driver = webdriver.Safari(options=options)
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 20)
            logger.info("Safari WebDriver setup complete!")
            
        except Exception as e:
            logger.error(f"Error setting up Safari WebDriver: {str(e)}")
            raise
        
    def login(self):
        """Navigate directly to Google Maps since user is already logged in."""
        try:
            logger.info("Navigating to Google Maps...")
            self.driver.get("https://www.google.com/maps")
            time.sleep(3)  # Wait for page to load
            logger.info("Successfully loaded Google Maps!")
            
        except Exception as e:
            logger.error(f"Error navigating to Google Maps: {str(e)}")
            raise
        
    def navigate_to_saved_places(self):
        """Navigate to the saved places section."""
        try:
            logger.info("Clicking 'Saved' button...")
            saved_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//div[contains(text(), 'Saved')]]"))
            )
            saved_button.click()
            time.sleep(5)  # Wait for saved menu to load
            
            logger.info("Clicking 'Favorites' button...")
            favorites_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//div[contains(text(), 'Favorites')] or .//div[contains(text(), 'Starred')]]"))
            )
            favorites_button.click()
            time.sleep(8)  # Wait for favorites to load
            
            logger.info("Successfully navigated to favorites!")
            
        except Exception as e:
            logger.error(f"Error navigating to favorites: {str(e)}")
            raise

    def extract_place_details(self, place_element):
        """Extract detailed information about a place."""
        try:
            # Extract basic info from the list item first
            try:
                name = place_element.find_element(By.CSS_SELECTOR, "div.qBF1Pd, div.fontHeadlineSmall").text.strip()
            except NoSuchElementException:
                name = place_element.find_element(By.CSS_SELECTOR, "div.fontHeadlineLarge").text.strip()
            
            logger.info(f"Extracting details for: {name}")
            
            # Click on the place to open its details
            place_element.click()
            time.sleep(3)  # Wait for details to load
            
            # Extract place information with retries
            max_retries = 3
            for _ in range(max_retries):
                try:
                    place_data = {
                        'name': name,
                        'address': self.safe_extract_text("button[data-item-id='address'], div[data-item-id='address']"),
                        'phone': self.safe_extract_text("button[data-item-id*='phone'], div[data-item-id*='phone']"),
                        'website': self.safe_extract_text("a[data-item-id='authority'], div[data-item-id='authority'] a"),
                        'rating': self.safe_extract_text("span.ceNzKf, span.fontDisplayLarge"),
                        'reviews_count': self.safe_extract_text("button[jsaction*='pane.rating.moreReviews'], div[jsaction*='pane.rating.moreReviews']"),
                        'category': self.safe_extract_text("button[jsaction*='categoryClick'], div[jsaction*='categoryClick']"),
                        'price_level': self.safe_extract_text("span[aria-label*='Price'], span.rogA2c"),
                        'scraped_at': datetime.now().isoformat()
                    }
                    
                    # If we got most of the data, break the retry loop
                    if place_data['address'] or place_data['phone'] or place_data['website']:
                        break
                    time.sleep(1)
                except Exception as e:
                    logger.warning(f"Retry {_ + 1} failed for {name}: {str(e)}")
                    if _ == max_retries - 1:  # Last retry
                        raise
                    time.sleep(1)
            
            # Extract opening hours if available
            try:
                hours_button = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-item-id*='oh'], div[data-item-id*='oh']"))
                )
                hours_button.click()
                time.sleep(1)
                hours = self.safe_extract_text("div.t39EBf, table.WgFkxc")
                place_data['opening_hours'] = hours
            except (NoSuchElementException, TimeoutException):
                place_data['opening_hours'] = None
            
            # Close the details panel to prepare for next place
            try:
                close_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Close'], button[jsaction*='pane.close']"))
                )
                close_button.click()
                time.sleep(1)
            except (NoSuchElementException, TimeoutException):
                logger.warning(f"Could not find close button for {name}")
            
            return place_data
            
        except Exception as e:
            logger.error(f"Error extracting details for place: {str(e)}")
            return None
        
    def safe_extract_text(self, selector):
        """Safely extract text from an element."""
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            return element.text
        except NoSuchElementException:
            return None
            
    def scrape_saved_places(self):
        """Main method to scrape all saved places."""
        try:
            logger.info("Starting the scraping process...")
            self.setup_driver()
            self.login()
            self.navigate_to_saved_places()
            
            # Wait for places to load
            logger.info("Waiting for places to load...")
            time.sleep(5)
            
            # Get all saved places - updated selector to match current structure
            logger.info("Looking for places in the favorites list...")
            place_elements = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.m6QErb div[role='article'], div.m6QErb div.Nv2PK"))
            )
            logger.info(f"Found {len(place_elements)} saved places")
            
            for i, place_element in enumerate(place_elements, 1):
                logger.info(f"Processing place {i}/{len(place_elements)}")
                try:
                    # Scroll element into view with offset to handle fixed headers
                    self.driver.execute_script("""
                        arguments[0].scrollIntoView(true);
                        window.scrollBy(0, -100);  // Scroll up a bit to handle fixed header
                    """, place_element)
                    time.sleep(1)  # Increased pause after scrolling
                    
                    # Ensure element is still valid and visible
                    if not place_element.is_displayed():
                        logger.warning(f"Place {i} is not visible, skipping...")
                        continue
                        
                    place_data = self.extract_place_details(place_element)
                    if place_data:
                        self.places.append(place_data)
                        logger.info(f"Successfully extracted details for: {place_data['name']}")
                    time.sleep(2)  # Increased delay between places
                except Exception as e:
                    logger.error(f"Error processing place {i}: {str(e)}")
                    continue
            
            # Save to CSV and JSON
            if self.places:
                # Save to CSV
                df = pd.DataFrame(self.places)
                csv_filename = f"google_maps_saved_places_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df.to_csv(csv_filename, index=False)
                logger.info(f"Successfully saved {len(self.places)} places to {csv_filename}")
                
                # Save to JSON
                json_filename = "output.json"
                with open(json_filename, 'w') as f:
                    json.dump(self.places, f, indent=2)
                logger.info(f"Successfully saved {len(self.places)} places to {json_filename}")
            
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            raise
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    try:
        scraper = GoogleMapsScraper()
        scraper.scrape_saved_places()
    except Exception as e:
        logger.error(f"Script failed: {str(e)}")
        if scraper.driver:
            scraper.driver.quit()
        sys.exit(1) 
        