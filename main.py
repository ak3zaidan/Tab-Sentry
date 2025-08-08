from camoufox.sync_api import Camoufox
from colorama import init, Fore, Style
import webbrowser
import threading
import asyncio
import random
import time
import sys
import os
import gc

try:
    import nodriver as nd
    from nodriver.cdp import fetch
    NODRIVER_AVAILABLE = True
except ImportError:
    NODRIVER_AVAILABLE = False

init(autoreset=True)

# Constants
RESI_PATH = "proxies.txt"
DISCORD_URL = "https://discord.gg/account-vaultx"
PROFILE_BUILDER_URL = "https://theprofilebuilder.com"
CHROMIUM_PATH = None  # Will use system default Chrome/Chromium
HEADLESS_MODE = False  # Set to True for headless mode

# Colors
PURPLE = Fore.MAGENTA
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
CYAN = Fore.CYAN
RESET = Style.RESET_ALL

# ASCII Art
art = r"""
   _____                                            __    ____   ____               .__     __   
  /  _  \    ____    ____    ____   __ __   ____  _/  |_  \   \ /   /_____    __ __ |  |  _/  |_ 
 /  /_\  \ _/ ___\ _/ ___\  /  _ \ |  |  \ /    \ \   __\  \   Y   / \__  \  |  |  \|  |  \   __|
/    |    \\  \___ \  \___ (  <_> )|  |  /|   |  \ |  |     \     /   / __ \_|  |  /|  |__ |  |  
\____|__  / \___  > \___  > \____/ |____/ |___|  / |__|      \___/   (____  /|____/ |____/ |__|  
        \/      \/      \/                     \/                         \/                     
"""

class AccountVaultApp:
    def __init__(self):
        self.proxies = []
        self.load_proxies()
        
    def display_banner(self):
        """Display the application banner"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(PURPLE + art + RESET)
        print(CYAN + "=" * 70 + RESET)
        print(GREEN + "Welcome to Account Vault Menu" + RESET)
        print(CYAN + "=" * 70 + RESET)
        print()
    
    def load_proxies(self):
        """Load proxies from the proxies file"""
        try:
            if not os.path.exists(RESI_PATH):
                print(f"{YELLOW}Warning: '{RESI_PATH}' not found. Proxy functionality will be disabled.{RESET}")
                return
            
            with open(RESI_PATH, "r", encoding='utf-8') as file:
                self.proxies = [line.strip() for line in file if line.strip()]
            
            if self.proxies:
                print(f"{GREEN}Loaded {len(self.proxies)} proxies from {RESI_PATH}{RESET}")
            else:
                print(f"{YELLOW}Warning: No valid proxies found in {RESI_PATH}{RESET}")
                
        except Exception as e:
            print(f"{RED}Error loading proxies: {str(e)}{RESET}")
    
    def parse_proxy(self, proxy_string):
        """Parse proxy string into components"""
        try:
            parts = proxy_string.split(':')
            if len(parts) >= 2:
                host = parts[0]
                port = parts[1]
                username = parts[2] if len(parts) > 2 else ""
                password = parts[3] if len(parts) > 3 else ""
                return host, port, username, password
            return "", "", "", ""
        except Exception:
            return "", "", "", ""
    
    def get_proxy_settings(self):
        """Get random proxy settings"""
        if not self.proxies:
            print(f"{RED}No proxies available{RESET}")
            return None
        
        try:
            proxy = random.choice(self.proxies)
            host, port, username, password = self.parse_proxy(proxy)
            
            if not host or not port:
                print(f"{RED}Invalid proxy format: {proxy}{RESET}")
                return None
            
            proxy_url = f"http://{host}:{port}"
            proxy_settings = {
                "server": proxy_url,
                "username": username,
                "password": password
            }
            
            print(f"{GREEN}Using proxy: {host}:{port}{RESET}")
            return proxy_settings
            
        except Exception as e:
            print(f"{RED}Error getting proxy: {str(e)}{RESET}")
            return None
    
    async def setup_proxy_auth(self, username, password, tab):
        """Setup proxy authentication for nodriver"""
        try:
            if username and password:
                print(f"{CYAN}Setting up proxy authentication...{RESET}")
                await tab.send(fetch.enable())
                await tab.send(fetch.enable(patterns=[fetch.RequestPattern(url_pattern="*", request_stage=fetch.RequestStage.REQUEST)]))
                
                # Handle auth challenges
                def handle_auth(event):
                    asyncio.create_task(tab.send(fetch.continue_request(
                        request_id=event.request_id,
                        headers=[
                            {"name": "Proxy-Authorization", "value": f"Basic {username}:{password}"}
                        ]
                    )))
                
                tab.add_handler(fetch.AuthRequired, handle_auth)
                print(f"{GREEN}Proxy authentication configured{RESET}")
        except Exception as e:
            print(f"{RED}Error setting up proxy auth: {str(e)}{RESET}")
    
    def open_discord_link(self):
        """Open Discord link in default browser"""
        try:
            print(f"{GREEN}Opening Discord link...{RESET}")
            webbrowser.open(DISCORD_URL)
            print(f"{GREEN}Discord link opened successfully!{RESET}")
        except Exception as e:
            print(f"{RED}Error opening Discord link: {str(e)}{RESET}")
    
    def open_profile_builder(self):
        """Open Profile Builder link in default browser"""
        try:
            print(f"{GREEN}Opening Profile Builder...{RESET}")
            webbrowser.open(PROFILE_BUILDER_URL)
            print(f"{GREEN}Profile Builder opened successfully!{RESET}")
        except Exception as e:
            print(f"{RED}Error opening Profile Builder: {str(e)}{RESET}")
    
    def open_stealth_tab(self):
        """Open a stealth browser tab with Camoufox using proxy"""
        def browser_thread():
            try:
                print(f"{YELLOW}Starting stealth browser...{RESET}")
                
                # Get proxy settings
                proxy_settings = self.get_proxy_settings()
                
                # Browser configuration
                config = {
                    "humanize": True
                }
                
                # Firefox preferences
                firefox_prefs = {
                    "media.peerconnection.enabled": False
                }
                
                print(f"{CYAN}Launching Camoufox browser...{RESET}")
                
                with Camoufox(
                    proxy=proxy_settings,
                    geoip=True,
                    config=config,
                    firefox_user_prefs=firefox_prefs
                ) as browser:
                    page = browser.new_page()
                    print(f"{GREEN}Browser launched successfully!{RESET}")
                    print(f"{CYAN}Navigating to Google...{RESET}")
                    
                    page.goto("https://www.google.com", wait_until="load")
                    print(f"{GREEN}Page loaded successfully! Browser is ready for use.{RESET}")
                    
                    # Keep the browser open until user closes it
                    print(f"{YELLOW}Browser is running. Close the browser window when done.{RESET}")
                    
                    # Wait for the browser to be closed
                    try:
                        while True:
                            try:
                                page.title()  # Check if page is still active
                                time.sleep(1)
                            except Exception:
                                break  # Browser was closed
                    except KeyboardInterrupt:
                        pass
                        
            except Exception as e:
                print(f"{RED}Error opening stealth browser: {str(e)}{RESET}")
                print(f"{RED}Make sure Camoufox is properly installed and configured.{RESET}")
        
        # Run browser in separate thread
        thread = threading.Thread(target=browser_thread, daemon=True)
        thread.start()
        print(f"{GREEN}Browser thread started. You can continue using the menu.{RESET}")
    
    def open_stealthy_chromium(self):
        """Open a stealthy Chromium window with nodriver using proxy"""
        if not NODRIVER_AVAILABLE:
            print(f"{RED}Error: nodriver is not installed. Please install it with: pip install nodriver{RESET}")
            return
        
        def chromium_thread():
            try:
                # Run the async chromium function
                asyncio.run(self._launch_chromium_browser())
            except Exception as e:
                print(f"{RED}Error in chromium thread: {str(e)}{RESET}")
        
        # Run chromium in separate thread
        thread = threading.Thread(target=chromium_thread, daemon=True)
        thread.start()
        print(f"{GREEN}Chromium browser thread started. You can continue using the menu.{RESET}")
    
    async def _launch_chromium_browser(self):
        """Launch Chromium browser with stealth settings"""
        browser = None
        tab = None
        
        try:
            print(f"{YELLOW}Starting stealthy Chromium browser...{RESET}")
            
            # Select a random proxy if available
            proxy = None
            proxy_creds = ["", ""]
            if self.proxies:
                proxy = random.choice(self.proxies)
                host, port, username, password = self.parse_proxy(proxy)
                proxy_creds = [username, password]
                print(f"{GREEN}Using proxy: {host}:{port}{RESET}")
            else:
                print(f"{YELLOW}Not using proxy{RESET}")
            
            # Randomize window size and position for unique fingerprint
            window_width = random.randint(1000, 1500)
            window_height = random.randint(750, 950)
            x_position = random.randint(0, 500)
            y_position = random.randint(0, 500)
            
            # Build Chrome arguments
            args = [
                f"--window-size={window_width},{window_height}",
                f"--window-position={x_position},{y_position}",
                "--disable-sync",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding",
                "--disable-background-timer-throttling",
                "--disable-breakpad",
                "--disable-extensions",
                "--incognito",
                "--disable-dev-shm-usage",
            ]
            
            # Inject proxy if used
            if proxy:
                host, port, username, password = self.parse_proxy(proxy)
                proxy_url = f"http://{host}:{port}"
                args.append(f"--proxy-server={proxy_url}")
                        
            # Start nodriver browser
            browser = await nd.start(
                browser_executable_path=CHROMIUM_PATH,
                headless=HEADLESS_MODE,
                stealth=True,
                browser_args=args
            )
            
            # Set up proxy authentication if needed
            if proxy and proxy_creds[0] and proxy_creds[1]:
                main_tab = await browser.get("data:,")
                await self.setup_proxy_auth(proxy_creds[0], proxy_creds[1], main_tab)
            
            print(f"{GREEN}Chromium browser launched successfully!{RESET}")
            print(f"{CYAN}Navigating to Google...{RESET}")
            
            # Navigate to Google
            tab = await browser.get("https://www.google.com")
            
            # Clear browser storage for clean session
            await tab.evaluate("""
                () => {
                    localStorage.clear();
                    sessionStorage.clear();
                }
            """)
            
            print(f"{GREEN}Page loaded successfully! Chromium browser is ready for use.{RESET}")
            print(f"{YELLOW}Browser is running. Close the browser window when done.{RESET}")
            
            # Keep the browser running until it's closed
            try:
                while True:
                    try:
                        await asyncio.sleep(1)
                    except Exception:
                        pass
            except Exception:
                pass
                
        except Exception as e:
            print(f"{RED}Error opening stealthy Chromium browser: {str(e)}{RESET}")
            print(f"{RED}Make sure Chrome/Chromium is installed and nodriver is properly configured.{RESET}")
        
        finally:
            # Thorough cleanup to ensure complete isolation between sessions
            if tab:
                try:
                    print(f"{CYAN}Cleaning up session...{RESET}")
                    # Execute cleanup JS
                    await tab.evaluate("""
                        () => {
                            try {
                                localStorage.clear();
                                sessionStorage.clear();
                                // Clear IndexedDB
                                if (indexedDB?.databases) {
                                    indexedDB.databases().then(dbs => {
                                        dbs.forEach(db => {
                                            if (db.name) indexedDB.deleteDatabase(db.name);
                                        });
                                    });
                                }
                                // Clear Cache Storage
                                if (caches?.keys) {
                                    caches.keys().then(keys => {
                                        keys.forEach(key => caches.delete(key));
                                    });
                                }
                                // Unregister Service Workers
                                if (navigator.serviceWorker?.getRegistrations) {
                                    navigator.serviceWorker.getRegistrations().then(regs => {
                                        regs.forEach(reg => reg.unregister());
                                    });
                                }
                                // Clear cookies manually
                                document.cookie.split(';').forEach(c => {
                                    document.cookie = c.trim().split('=')[0] + '=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/';
                                });
                            } catch (e) {
                                console.error('Error during JS cleanup:', e);
                            }
                        }
                    """)
                except Exception as e:
                    print(f"{YELLOW}Warning: Error during cleanup: {e}{RESET}")
                finally:
                    try:
                        if browser:
                            browser.stop()  # Stop the entire browser session
                            print(f"{GREEN}Browser session closed successfully.{RESET}")
                    except Exception as stop_error:
                        print(f"{RED}Error while closing browser: {stop_error}{RESET}")
                    
                    # Force garbage collection to free memory
                    gc.collect()
    
    def display_menu(self):
        """Display the main menu options"""
        print()
        print(PURPLE + "Choose an option:" + RESET)
        print(f"{GREEN}1.{RESET} Join Account Vault Discord")
        print(f"{GREEN}2.{RESET} Visit The Profile Builder")  
        print(f"{GREEN}3.{RESET} Open Stealth Browser Tab")
        print(f"{GREEN}4.{RESET} Open Stealthy Chromium Window")
        print(f"{RED}5.{RESET} Exit")
        print()
    
    def get_user_choice(self):
        """Get and validate user input"""
        while True:
            try:
                choice = input(f"{CYAN}Enter your choice (1-5): {RESET}").strip()
                
                if choice in ['1', '2', '3', '4', '5']:
                    return int(choice)
                else:
                    print(f"{RED}Invalid choice. Please enter 1, 2, 3, 4, or 5.{RESET}")
                    
            except KeyboardInterrupt:
                print(f"\n{YELLOW}Exiting...{RESET}")
                sys.exit(0)
            except Exception as e:
                print(f"{RED}Error reading input: {str(e)}. Please try again.{RESET}")
    
    def process_choice(self, choice):
        """Process the user's menu choice"""
        if choice == 1:
            self.open_discord_link()
        elif choice == 2:
            self.open_profile_builder()
        elif choice == 3:
            self.open_stealth_tab()
        elif choice == 4:
            self.open_stealthy_chromium()
        elif choice == 5:
            print(f"{YELLOW}Thanks for using Account Vault Menu! Goodbye!{RESET}")
            sys.exit(0)
    
    def wait_for_continue(self):
        """Wait for user to press Enter before continuing"""
        try:
            input(f"\n{CYAN}Press Enter to continue...{RESET}")
        except KeyboardInterrupt:
            print(f"\n{YELLOW}Exiting...{RESET}")
            sys.exit(0)
    
    def run(self):
        """Main application loop"""
        print(f"{GREEN}Application started successfully!{RESET}")
        
        # Show nodriver availability status
        if NODRIVER_AVAILABLE:
            print(f"{GREEN}nodriver is available - Chromium functionality enabled{RESET}")
        else:
            print(f"{YELLOW}nodriver is not installed - Chromium functionality will be limited{RESET}")
        
        while True:
            try:
                self.display_banner()
                self.display_menu()
                choice = self.get_user_choice()
                
                print(f"\n{CYAN}Processing your choice...{RESET}")
                self.process_choice(choice)
                
                self.wait_for_continue()
                
            except KeyboardInterrupt:
                print(f"\n{YELLOW}Application interrupted. Exiting...{RESET}")
                break
            except Exception as e:
                print(f"{RED}Unexpected error: {str(e)}{RESET}")
                self.wait_for_continue()

def main():
    """Main entry point"""
    try:
        app = AccountVaultApp()
        app.run()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Application terminated by user.{RESET}")
    except Exception as e:
        print(f"{RED}Fatal error: {str(e)}{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
