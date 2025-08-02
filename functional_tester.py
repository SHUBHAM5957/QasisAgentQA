import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import platform
import os
from typing import List, Dict, Any
from config import TARGET_WEBSITE, API_ENDPOINT, TEST_API_DATA, API_URL

class FunctionalTester:
    def __init__(self):
        self.driver = None
        self.test_results = []
        self.base_url = TARGET_WEBSITE
        
    def setup_driver(self):
        """Initialize the web driver with improved error handling"""
        try:
            # Method 1: Use webdriver-manager with specific architecture
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")
            
            # Try multiple approaches
            driver_created = False
            
            # Approach 1: Use webdriver-manager (most common solution)
            try:
                print("🔧 Attempting to setup driver using webdriver-manager...")
                
                # Clear cache and download fresh driver
                driver_path = ChromeDriverManager().install()
                print(f"📍 ChromeDriver installed at: {driver_path}")
                
                # Verify the driver file exists and is executable
                if not os.path.exists(driver_path):
                    raise Exception(f"Driver not found at path: {driver_path}")
                
                service = Service(driver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                self.driver.implicitly_wait(10)
                driver_created = True
                print("✅ Driver setup successful using webdriver-manager")
                
            except Exception as e:
                print(f"❌ webdriver-manager approach failed: {e}")
                
            # Approach 2: Try with system PATH ChromeDriver
            if not driver_created:
                try:
                    print("🔧 Attempting to use system PATH ChromeDriver...")
                    self.driver = webdriver.Chrome(options=chrome_options)
                    self.driver.implicitly_wait(10)
                    driver_created = True
                    print("✅ Driver setup successful using system PATH")
                    
                except Exception as e:
                    print(f"❌ System PATH approach failed: {e}")
            
            # Approach 3: Try with explicit driver path
            if not driver_created:
                try:
                    print("🔧 Attempting to use explicit ChromeDriver path...")
                    
                    # Common ChromeDriver locations on Windows
                    possible_paths = [
                        r"C:\Program Files\Google\Chrome\Application\chromedriver.exe",
                        r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe",
                        r"C:\chromedriver\chromedriver.exe",
                        r".\chromedriver.exe",
                        r"./drivers/chromedriver.exe"
                    ]
                    
                    for path in possible_paths:
                        if os.path.exists(path):
                            print(f"📍 Found ChromeDriver at: {path}")
                            service = Service(path)
                            self.driver = webdriver.Chrome(service=service, options=chrome_options)
                            self.driver.implicitly_wait(10)
                            driver_created = True
                            print("✅ Driver setup successful using explicit path")
                            break
                            
                except Exception as e:
                    print(f"❌ Explicit path approach failed: {e}")
            
            # Approach 4: Try Edge WebDriver as fallback
            if not driver_created:
                try:
                    print("🔧 Attempting to use Edge WebDriver as fallback...")
                    from selenium.webdriver.edge.service import Service as EdgeService
                    from selenium.webdriver.edge.options import Options as EdgeOptions
                    from webdriver_manager.microsoft import EdgeChromiumDriverManager
                    
                    edge_options = EdgeOptions()
                    edge_options.add_argument("--headless")
                    edge_options.add_argument("--no-sandbox")
                    edge_options.add_argument("--disable-dev-shm-usage")
                    edge_options.add_argument("--disable-gpu")
                    edge_options.add_argument("--window-size=1920,1080")
                    
                    edge_service = EdgeService(EdgeChromiumDriverManager().install())
                    self.driver = webdriver.Edge(service=edge_service, options=edge_options)
                    self.driver.implicitly_wait(10)
                    driver_created = True
                    print("✅ Driver setup successful using Edge WebDriver")
                    
                except Exception as e:
                    print(f"❌ Edge WebDriver approach failed: {e}")
            
            # Approach 5: Try Firefox as final fallback
            if not driver_created:
                try:
                    print("🔧 Attempting to use Firefox WebDriver as final fallback...")
                    from selenium.webdriver.firefox.service import Service as FirefoxService
                    from selenium.webdriver.firefox.options import Options as FirefoxOptions
                    from webdriver_manager.firefox import GeckoDriverManager
                    
                    firefox_options = FirefoxOptions()
                    firefox_options.add_argument("--headless")
                    firefox_options.add_argument("--no-sandbox")
                    firefox_options.add_argument("--disable-dev-shm-usage")
                    
                    firefox_service = FirefoxService(GeckoDriverManager().install())
                    self.driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
                    self.driver.implicitly_wait(10)
                    driver_created = True
                    print("✅ Driver setup successful using Firefox WebDriver")
                    
                except Exception as e:
                    print(f"❌ Firefox WebDriver approach failed: {e}")
            
            if not driver_created:
                raise Exception("All WebDriver setup approaches failed")
                
            return True
            
        except Exception as e:
            print(f"❌ Failed to setup driver: {e}")
            self.print_troubleshooting_guide()
            return False
    
    def print_troubleshooting_guide(self):
        """Print troubleshooting guide for WebDriver issues"""
        print("\n" + "="*50)
        print("🔧 TROUBLESHOOTING GUIDE")
        print("="*50)
        print("The WebDriver setup failed. Here are some solutions:")
        print("\n1. INSTALL/UPDATE CHROME:")
        print("   - Make sure Google Chrome is installed and updated")
        print("   - Download from: https://www.google.com/chrome/")
        
        print("\n2. CLEAR WEBDRIVER CACHE:")
        print("   - Delete the webdriver cache folder:")
        print(f"   - Windows: C:\\Users\\{os.getenv('USERNAME', 'YourUser')}\\.wdm\\")
        print("   - Run: pip uninstall webdriver-manager && pip install webdriver-manager")
        
        print("\n3. MANUAL CHROMEDRIVER INSTALLATION:")
        print("   - Go to: https://chromedriver.chromium.org/")
        print("   - Download ChromeDriver matching your Chrome version")
        print("   - Extract to a folder (e.g., C:\\chromedriver\\)")
        print("   - Add the folder to your system PATH")
        
        print("\n4. CHECK SYSTEM ARCHITECTURE:")
        print(f"   - Your system: {platform.machine()}")
        print(f"   - Python architecture: {platform.architecture()[0]}")
        print("   - Ensure ChromeDriver matches your system architecture")
        
        print("\n5. ALTERNATIVE SOLUTIONS:")
        print("   - Try running as administrator")
        print("   - Disable antivirus temporarily")
        print("   - Use Edge or Firefox instead of Chrome")
        print("   - Use Docker with Selenium Grid")
        
        print("\n6. INSTALL EDGE OR FIREFOX AS BACKUP:")
        print("   - Edge: Usually pre-installed on Windows")
        print("   - Firefox: https://www.mozilla.org/firefox/")
        print("="*50)
    
    def navigate_to_website(self):
        """Navigate to the target website"""
        try:
            print(f"🌐 Navigating to: {self.base_url}")
            self.driver.get(self.base_url)
            time.sleep(3)
            
            # Check if page loaded successfully
            if "error" in self.driver.title.lower() or "not found" in self.driver.title.lower():
                self.test_results.append({
                    "type": "error",
                    "category": "navigation",
                    "description": f"Failed to load website: {self.driver.title}",
                    "severity": "critical"
                })
                return False
            
            print(f"✅ Successfully loaded: {self.driver.title}")
            return True
        except Exception as e:
            self.test_results.append({
                "type": "error",
                "category": "navigation",
                "description": f"Navigation failed: {str(e)}",
                "severity": "critical"
            })
            return False
    
    def test_clickable_elements(self):
        """Test all clickable elements on the page"""
        print("🔍 Testing clickable elements...")
        
        try:
            # Find all clickable elements
            links = self.driver.find_elements(By.TAG_NAME, "a")
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='submit'], input[type='button']")
            
            all_elements = links + buttons + inputs
            
            for element in all_elements:
                try:
                    # Check if element is visible and clickable
                    if element.is_displayed() and element.is_enabled():
                        element_text = element.text or element.get_attribute("aria-label") or "Unknown"
                        element_type = element.tag_name
                        
                        # Try to click the element
                        try:
                            self.driver.execute_script("arguments[0].scrollIntoView();", element)
                            time.sleep(1)
                            
                            # Check if clicking would navigate away
                            current_url = self.driver.current_url
                            element.click()
                            time.sleep(2)
                            
                            new_url = self.driver.current_url
                            if new_url != current_url:
                                print(f"✅ {element_type}: '{element_text}' - Navigation successful")
                                self.driver.back()
                                time.sleep(1)
                            else:
                                print(f"✅ {element_type}: '{element_text}' - Click successful")
                                
                        except Exception as click_error:
                            self.test_results.append({
                                "type": "bug",
                                "category": "clickable_elements",
                                "description": f"Failed to click {element_type}: '{element_text}' - {str(click_error)}",
                                "severity": "medium"
                            })
                            
                except Exception as e:
                    continue
                    
        except Exception as e:
            self.test_results.append({
                "type": "error",
                "category": "clickable_elements",
                "description": f"Error testing clickable elements: {str(e)}",
                "severity": "high"
            })
    
    def test_forms(self):
        """Test all forms on the page"""
        print("📝 Testing forms...")
        
        try:
            forms = self.driver.find_elements(By.TAG_NAME, "form")
            
            for form in forms:
                try:
                    form_id = form.get_attribute("id") or form.get_attribute("name") or "Unknown Form"
                    inputs = form.find_elements(By.TAG_NAME, "input")
                    textareas = form.find_elements(By.TAG_NAME, "textarea")
                    selects = form.find_elements(By.TAG_NAME, "select")
                    
                    all_form_elements = inputs + textareas + selects
                    
                    print(f"🔍 Testing form: {form_id}")
                    
                    # Test form validation
                    for element in all_form_elements:
                        element_type = element.get_attribute("type") or element.tag_name
                        element_name = element.get_attribute("name") or element.get_attribute("id") or "Unknown"
                        
                        # Test required fields
                        if element.get_attribute("required"):
                            try:
                                element.clear()
                                # Try to submit form without filling required field
                                submit_button = form.find_element(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
                                submit_button.click()
                                time.sleep(1)
                                
                                # Check for validation message
                                validation_messages = self.driver.find_elements(By.CSS_SELECTOR, ".error, .validation-error, [role='alert']")
                                if validation_messages:
                                    print(f"✅ Form validation working for {element_name}")
                                else:
                                    self.test_results.append({
                                        "type": "bug",
                                        "category": "form_validation",
                                        "description": f"Missing validation for required field: {element_name}",
                                        "severity": "medium"
                                    })
                                    
                            except Exception as e:
                                continue
                                
                except Exception as e:
                    self.test_results.append({
                        "type": "error",
                        "category": "forms",
                        "description": f"Error testing form: {str(e)}",
                        "severity": "medium"
                    })
                    
        except Exception as e:
            self.test_results.append({
                "type": "error",
                "category": "forms",
                "description": f"Error testing forms: {str(e)}",
                "severity": "high"
            })
    
    def test_api_endpoint(self):
        """Test the API endpoint with exact cURL request replication"""
        print("🔌 Testing API endpoint...")
        
        # Construct full API URL
        full_api_url = API_URL.rstrip('/') + '/' + API_ENDPOINT.lstrip('/')
        
        try:
            # Headers exactly matching the cURL request
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Origin': 'http://localhost:3000',
                'Referer': 'http://localhost:3000/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"'
            }
            
            print(f"📤 Sending POST request to: {full_api_url}")
            print(f"📋 Payload preview: {TEST_API_DATA['content'][:100]}...")
            
            response = requests.post(full_api_url, json=TEST_API_DATA, headers=headers, timeout=30)
            
            if response.status_code == 200:
                print("✅ API endpoint responded successfully")
                try:
                    result = response.json()
                    print(f"📊 API Response (JSON): {json.dumps(result, indent=2)}")
                except json.JSONDecodeError:
                    print(f"📊 API Response (Text): {response.text}")
                    
                # Log the successful test
                self.test_results.append({
                    "type": "success",
                    "category": "api",
                    "description": f"API endpoint responded with status 200",
                    "severity": "info"
                })
                
            elif response.status_code == 404:
                self.test_results.append({
                    "type": "error",
                    "category": "api",
                    "description": f"API endpoint not found (404). Check if the server is running on port 8080",
                    "severity": "critical"
                })
                
            elif response.status_code == 500:
                self.test_results.append({
                    "type": "bug",
                    "category": "api",
                    "description": f"API endpoint returned internal server error (500). Response: {response.text}",
                    "severity": "high"
                })
                
            else:
                self.test_results.append({
                    "type": "bug",
                    "category": "api",
                    "description": f"API endpoint returned unexpected status code: {response.status_code}. Response: {response.text}",
                    "severity": "high"
                })
                
        except requests.exceptions.ConnectionError as e:
            self.test_results.append({
                "type": "error",
                "category": "api",
                "description": f"API endpoint is not accessible - Connection refused. Make sure the server is running on localhost:8080. Error: {str(e)}",
                "severity": "critical"
            })
            
        except requests.exceptions.Timeout as e:
            self.test_results.append({
                "type": "error",
                "category": "api",
                "description": f"API endpoint request timed out after 30 seconds. Error: {str(e)}",
                "severity": "high"
            })
            
        except Exception as e:
            self.test_results.append({
                "type": "error",
                "category": "api",
                "description": f"API testing failed with unexpected error: {str(e)}",
                "severity": "high"
            })
    
    def run_functional_tests(self):
        """Run all functional tests"""
        print("🚀 Starting Functional Testing...")
        print(f"🎯 Target Website: {self.base_url}")
        print(f"🔌 API URL: {API_URL}")
        print(f"🔌 API Endpoint: {API_ENDPOINT}")
        print(f"🔌 Full API URL: {API_URL.rstrip('/') + '/' + API_ENDPOINT.lstrip('/')}")
        
        if not self.setup_driver():
            print("⚠️ Skipping browser tests due to WebDriver setup failure")
            # Still run API tests even if browser setup fails
            self.test_api_endpoint()
            return self.test_results
        
        try:
            if self.navigate_to_website():
                self.test_clickable_elements()
                self.test_forms()
            else:
                self.test_results.append({
                    "type": "error",
                    "category": "navigation",
                    "description": "Cannot proceed with browser-based functional tests due to navigation failure",
                    "severity": "critical"
                })
                
            # Always test API endpoint regardless of browser test results
            self.test_api_endpoint()
            
        finally:
            if self.driver:
                self.driver.quit()
                print("🔚 WebDriver session closed")
        
        print(f"✅ Functional testing completed. Found {len([r for r in self.test_results if r['type'] != 'success'])} issues.")
        return self.test_results

# Usage example
if __name__ == "__main__":
    tester = FunctionalTester()
    results = tester.run_functional_tests()
    
    # Print detailed summary
    print("\n" + "="*60)
    print("📊 FUNCTIONAL TEST RESULTS SUMMARY")
    print("="*60)
    
    if results:
        # Categorize results
        errors = [r for r in results if r['type'] == 'error']
        bugs = [r for r in results if r['type'] == 'bug']
        successes = [r for r in results if r['type'] == 'success']
        
        if successes:
            print(f"\n✅ Successful Tests ({len(successes)}):")
            for result in successes:
                print(f"  ✓ {result['category']}: {result['description']}")
        
        if errors:
            print(f"\n❌ Critical Errors ({len(errors)}):")
            for result in errors:
                print(f"  ❌ {result['category']}: {result['description']} (Severity: {result['severity']})")
        
        if bugs:
            print(f"\n🐛 Bugs Found ({len(bugs)}):")
            for result in bugs:
                print(f"  🐛 {result['category']}: {result['description']} (Severity: {result['severity']})")
                
        print(f"\n📈 Overall Status:")
        print(f"  - Total Tests: {len(results)}")
        print(f"  - Successful: {len(successes)}")
        print(f"  - Issues Found: {len(errors) + len(bugs)}")
        print(f"  - Critical Issues: {len([r for r in results if r['severity'] == 'critical'])}")
        
    else:
        print("\n🎉 No test results found - this might indicate a setup issue")
    
    print("="*60)