"""
Safari automation module using AppleScript.
"""
import subprocess
from typing import Optional

class SafariAutomation:
    def __init__(self):
        self.applescript_template = """
        tell application "Safari"
            activate
            {command}
        end tell
        """

    def execute_applescript(self, command: str) -> Optional[str]:
        """
        Execute AppleScript command in Safari.
        
        Args:
            command: The AppleScript command to execute
            
        Returns:
            Optional[str]: The result of the AppleScript execution
        """
        full_script = self.applescript_template.format(command=command)
        try:
            result = subprocess.run(
                ["osascript", "-e", full_script],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error executing AppleScript: {e}")
            return None

    def navigate_to_url(self, url: str) -> bool:
        """
        Navigate Safari to a specific URL using the existing window.
        
        Args:
            url: The URL to navigate to
            
        Returns:
            bool: True if navigation was successful
        """
        command = f"""
        activate
        if (count of windows) = 0 then
            make new document
        end if
        tell window 1
            set current tab to make new tab with properties {{URL:"{url}"}}
        end tell
        """
        return self.execute_applescript(command) is not None

    def get_current_url(self) -> Optional[str]:
        """
        Get the current URL of the active Safari tab.
        
        Returns:
            Optional[str]: The current URL
        """
        command = """
        tell window 1
            return URL of current tab
        end tell
        """
        return self.execute_applescript(command)

    def check_login_state(self) -> bool:
        """
        Check if we're logged into Google Maps.
        
        Returns:
            bool: True if logged in, False otherwise
        """
        # Check for the specific Google Account link that appears when logged in
        command = """
        tell window 1
            set loginCheck to do JavaScript "
                (function() {
                    // Check for Google Account link with email
                    const accountLink = document.querySelector('a.gb_B.gb_Za[aria-label*=\\"Google Account\\"]');
                    if (accountLink && accountLink.getAttribute('aria-label').includes('jhw513@gmail.com')) {
                        return true;
                    }
                    
                    // Check for profile image
                    const profileImg = document.querySelector('img.gb_P.gbii[src*=\\"googleusercontent.com\\"]');
                    if (profileImg) {
                        return true;
                    }
                    
                    return false;
                })()
            " in current tab
            return loginCheck
        end tell
        """
        result = self.execute_applescript(command)
        return result == "true"

    def wait_for_element(self, selector: str, timeout: int = 10) -> bool:
        """
        Wait for an element to appear on the page.
        
        Args:
            selector: CSS selector to wait for
            timeout: Maximum time to wait in seconds
            
        Returns:
            bool: True if element appeared
        """
        # Escape quotes in the selector for JavaScript
        escaped_selector = selector.replace('"', '\\"')
        command = f"""
        tell window 1
            set startTime to current date
            repeat until (do JavaScript "document.querySelector('{escaped_selector}') !== null" in current tab) is "true"
                if (current date) - startTime > {timeout} then
                    return false
                end if
                delay 0.5
            end repeat
            return true
        end tell
        """
        result = self.execute_applescript(command)
        return result == "true" 