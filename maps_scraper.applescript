tell application "Safari"
	activate
	
	-- Make sure we have a window
	if (count of windows) = 0 then
		make new document
	end if
	
	-- Start logging
	log "🚀 Starting Google Maps Scraper..."
	
	-- Navigate to Google Maps main page first
	set mapsURL to "https://www.google.com/maps"
	
	tell window 1
		set current tab to (make new tab with properties {URL:mapsURL})
		log "🌐 Opening Google Maps..."
		delay 5 -- Increased initial page load delay
		
		-- Wait for the page to be fully loaded
		log "⏳ Waiting for page to load..."
		repeat until (do JavaScript "document.readyState" in current tab) is "complete"
			delay 1
		end repeat
		
		-- Additional delay to ensure all dynamic content is loaded
		delay 5
		
		-- Try to find and click the Saved button
		log "🔍 Looking for Saved button..."
		set savedButtonResult to do JavaScript "(() => {
			const waitForElement = (selector, maxAttempts = 10) => {
				let attempts = 0;
				const element = Array.from(document.querySelectorAll('button')).find(btn => 
					btn.textContent.includes('Saved') && 
					btn.closest('.wR3cXd')  // Navigation rail button class
				);
				if (element) return element;
				if (attempts < maxAttempts) {
					attempts++;
					return null;
				}
				return null;
			};
			
			const button = waitForElement('button');
			if (!button) return { buttonFound: false };
			
			return {
				buttonFound: true,
				buttonText: button.textContent,
				html: button.outerHTML
			};
		})()" in current tab
		
		log "📝 Saved button debug info:"
		log savedButtonResult
		
		if savedButtonResult's buttonFound then
			log "🖱️ Clicking Saved button..."
			do JavaScript "(() => {
				const button = Array.from(document.querySelectorAll('button')).find(btn => 
					btn.textContent.includes('Saved') && 
					btn.closest('.wR3cXd')
				);
				if (button) {
					button.click();
					return true;
				}
				return false;
			})()" in current tab
			
			delay 8 -- Increased delay after clicking Saved button
			
			-- Try to find and click the Favorites button
			log "🔍 Looking for Favorites button..."
			set favoritesResult to do JavaScript "(() => {
				let maxAttempts = 10;
				let attempts = 0;
				let button = null;
				
				while (attempts < maxAttempts) {
					button = Array.from(document.querySelectorAll('button')).find(btn => 
						(btn.textContent || '').includes('Favorites') || 
						(btn.textContent || '').includes('Starred')
					);
					if (button) break;
					attempts++;
				}
				
				if (!button) return { buttonFound: false };
				
				button.click();
				return { 
					buttonFound: true,
					buttonText: button.textContent,
					html: button.outerHTML 
				};
			})()" in current tab
			
			log "📝 Favorites button debug info:"
			log favoritesResult
			
			delay 8 -- Wait for favorites to load
			
			log "🔍 Looking for list items..."
			set listResult to do JavaScript "(() => {
				// Function to wait for elements to be loaded
				const waitForElements = (selector, maxAttempts = 10) => {
					let attempts = 0;
					const elements = document.querySelectorAll(selector);
					if (elements.length > 0) return Array.from(elements);
					if (attempts < maxAttempts) {
						attempts++;
						return null;
					}
					return [];
				};
				
				// Try to find list items with retry
				const listItems = waitForElements('.xkqFBc') || [];
				
				const debug = {
					listItemsFound: listItems.length,
					firstListItemHtml: listItems.length > 0 ? listItems[0].outerHTML : null,
					allButtons: Array.from(document.querySelectorAll('button')).map(btn => btn.textContent).filter(text => text),
					visibleText: Array.from(document.querySelectorAll('*')).map(el => el.textContent).filter(text => text)
				};
				
				return {
					items: listItems.map(item => {
						const nameEl = item.querySelector('.cGRe9e');
						const countEl = item.querySelector('.aJVa5c');
						return {
							name: nameEl ? nameEl.textContent.trim() : '',
							count: countEl ? countEl.textContent.trim() : '',
							html: item.outerHTML
						};
					}),
					debug: debug
				};
			})()" in current tab
			
			log "📝 List items found:"
			log listResult
			
			-- Additional delay before finishing
			delay 3
		end if
	end tell
end tell

log "✅ Done!" 