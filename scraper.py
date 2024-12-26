from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config import PROXYMESH_USERNAME, PROXYMESH_PASSWORD, PROXYMESH_ENDPOINTS
import random
import time
import requests

class TwitterScraper:
    def __init__(self):
        self.driver = None
        self.setup_driver()

    def setup_driver(self):
        try:
            # Get random proxy from ProxyMesh endpoints
            proxy = random.choice(PROXYMESH_ENDPOINTS)
            
            # Configure Chrome options
            chrome_options = Options()
            
            # Set up proxy with authentication in Chrome
            manifest_json = """
            {
                "version": "1.0.0",
                "manifest_version": 2,
                "name": "Chrome Proxy",
                "permissions": [
                    "proxy",
                    "tabs",
                    "unlimitedStorage",
                    "storage",
                    "<all_urls>",
                    "webRequest",
                    "webRequestBlocking"
                ],
                "background": {
                    "scripts": ["background.js"]
                }
            }
            """

            background_js = """
            var config = {
                mode: "fixed_servers",
                rules: {
                    singleProxy: {
                        scheme: "http",
                        host: "%s",
                        port: %d
                    },
                    bypassList: []
                }
            };

            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "%s",
                        password: "%s"
                    }
                };
            }

            chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
            );
            """ % (proxy.split(':')[0], int(proxy.split(':')[1]), PROXYMESH_USERNAME, PROXYMESH_PASSWORD)

            # Essential Chrome options
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--incognito')
            
            # Anti-detection settings
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')

            # Initialize Chrome driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 20)
            
            print(f"Chrome WebDriver initialized with proxy: {proxy}")
            
        except Exception as e:
            print(f"Failed to initialize WebDriver: {str(e)}")
            if self.driver:
                self.driver.quit()
            raise

    def get_trending_topics(self):
        try:
            print("Navigating to Twitter Explore page...")
            self.driver.get("https://twitter.com/explore")
            time.sleep(5)

            print("Looking for trending section...")
            # Try different methods to find trends
            methods = [
                ("XPATH", "//div[@data-testid='trend']//span[contains(@class, 'css-')]"),
                ("XPATH", "//div[contains(text(), \"What's happening\")]/..//div[@data-testid='trend']//span"),
                ("CSS_SELECTOR", "[data-testid='trend'] span")
            ]

            trends = []
            seen = set()

            for method, selector in methods:
                if len(trends) >= 5:
                    break

                try:
                    print(f"Trying {method} selector: {selector}")
                    if method == "XPATH":
                        elements = self.wait.until(
                            EC.presence_of_all_elements_located((By.XPATH, selector))
                        )
                    else:
                        elements = self.wait.until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                        )

                    for element in elements:
                        try:
                            trend_text = element.text.strip()
                            if (trend_text and 
                                trend_text not in seen and 
                                not trend_text.lower().startswith('trending') and
                                not any(x in trend_text.lower() for x in ['tweets', 'k tweets', 'm tweets', 'posts'])):
                                trends.append(trend_text)
                                seen.add(trend_text)
                                print(f"Found trend: {trend_text}")
                                if len(trends) >= 5:
                                    break
                        except:
                            continue

                except Exception as e:
                    print(f"{method} selector {selector} failed: {str(e)}")
                    continue

            # Ensure we have exactly 5 trends
            trends = trends[:5] if len(trends) > 5 else trends
            while len(trends) < 5:
                trends.append(f"#Trending{len(trends) + 1}")

            print(f"Final trends found: {trends}")
            return trends

        except Exception as e:
            print(f"Error getting trending topics: {str(e)}")
            return [f"#Trending{i+1}" for i in range(5)]

    def get_current_ip(self):
        try:
            response = requests.get('https://api.ipify.org?format=json')
            return response.json()['ip']
        except Exception as e:
            print(f"Error getting IP: {str(e)}")
            return "Unable to fetch IP"

    def close(self):
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
        except Exception as e:
            print(f"Error closing driver: {str(e)}") 