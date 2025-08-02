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
from typing import List, Dict, Any
from config import TARGET_WEBSITE, API_ENDPOINT, TEST_API_DATA

class FunctionalTester:
    def __init__(self):
        self.driver = None
        self.test_results = []
        self.base_url = TARGET_WEBSITE
        
    def setup_driver(self):
        """Initialize the web driver"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(10)
            return True
        except Exception as e:
            print(f"❌ Failed to setup driver: {e}")
            return False
    
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
        """Test the API endpoint"""
        print("🔌 Testing API endpoint...")
        
        try:
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
            
            response = requests.post(API_ENDPOINT, json=TEST_API_DATA, headers=headers, timeout=30)
            
            if response.status_code == 200:
                print("✅ API endpoint responded successfully")
                try:
                    result = response.json()
                    print(f"📊 API Response: {json.dumps(result, indent=2)}")
                except:
                    print(f"📊 API Response: {response.text}")
            else:
                self.test_results.append({
                    "type": "bug",
                    "category": "api",
                    "description": f"API endpoint returned status code: {response.status_code}",
                    "severity": "high"
                })
                
        except requests.exceptions.ConnectionError:
            self.test_results.append({
                "type": "error",
                "category": "api",
                "description": "API endpoint is not accessible (Connection refused)",
                "severity": "critical"
            })
        except Exception as e:
            self.test_results.append({
                "type": "error",
                "category": "api",
                "description": f"API testing failed: {str(e)}",
                "severity": "high"
            })
    
    def run_functional_tests(self):
        """Run all functional tests"""
        print("🚀 Starting Functional Testing...")
        
        if not self.setup_driver():
            return self.test_results
        
        try:
            if self.navigate_to_website():
                self.test_clickable_elements()
                self.test_forms()
                self.test_api_endpoint()
            else:
                self.test_results.append({
                    "type": "error",
                    "category": "navigation",
                    "description": "Cannot proceed with functional tests due to navigation failure",
                    "severity": "critical"
                })
        finally:
            if self.driver:
                self.driver.quit()
        
        print(f"✅ Functional testing completed. Found {len(self.test_results)} issues.")
        return self.test_results 