import requests
import time
import json
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from config import TARGET_WEBSITE, API_ENDPOINT

class NonFunctionalTester:
    def __init__(self):
        self.test_results = []
        self.base_url = TARGET_WEBSITE
        
    def measure_performance(self):
        """Measure website performance metrics"""
        print("⚡ Measuring performance...")
        
        try:
            start_time = time.time()
            response = requests.get(self.base_url, timeout=30)
            load_time = time.time() - start_time
            
            # Performance metrics
            response_time = response.elapsed.total_seconds()
            page_size = len(response.content)
            
            print(f"📊 Performance Metrics:")
            print(f"   - Load Time: {load_time:.2f} seconds")
            print(f"   - Response Time: {response_time:.2f} seconds")
            print(f"   - Page Size: {page_size / 1024:.2f} KB")
            
            # Performance thresholds
            if load_time > 5:
                self.test_results.append({
                    "type": "performance_issue",
                    "category": "load_time",
                    "description": f"Page load time is too slow: {load_time:.2f} seconds",
                    "severity": "high"
                })
            
            if response_time > 2:
                self.test_results.append({
                    "type": "performance_issue",
                    "category": "response_time",
                    "description": f"Server response time is slow: {response_time:.2f} seconds",
                    "severity": "medium"
                })
            
            if page_size > 1024 * 1024:  # 1MB
                self.test_results.append({
                    "type": "performance_issue",
                    "category": "page_size",
                    "description": f"Page size is too large: {page_size / 1024 / 1024:.2f} MB",
                    "severity": "medium"
                })
                
        except requests.exceptions.Timeout:
            self.test_results.append({
                "type": "performance_issue",
                "category": "timeout",
                "description": "Website took too long to respond (timeout)",
                "severity": "critical"
            })
        except Exception as e:
            self.test_results.append({
                "type": "error",
                "category": "performance",
                "description": f"Performance testing failed: {str(e)}",
                "severity": "high"
            })
    
    def security_scan(self):
        """Perform basic security scan"""
        print("🔒 Performing security scan...")
        
        try:
            response = requests.get(self.base_url, timeout=30)
            
            # Check security headers
            security_headers = {
                'X-Frame-Options': 'Missing X-Frame-Options header (clickjacking protection)',
                'X-Content-Type-Options': 'Missing X-Content-Type-Options header (MIME sniffing protection)',
                'X-XSS-Protection': 'Missing X-XSS-Protection header (XSS protection)',
                'Strict-Transport-Security': 'Missing HSTS header (HTTPS enforcement)',
                'Content-Security-Policy': 'Missing CSP header (content security policy)'
            }
            
            for header, message in security_headers.items():
                if header not in response.headers:
                    self.test_results.append({
                        "type": "security_vulnerability",
                        "category": "missing_security_headers",
                        "description": message,
                        "severity": "medium"
                    })
            
            # Check for HTTPS
            if not self.base_url.startswith('https://'):
                self.test_results.append({
                    "type": "security_vulnerability",
                    "category": "https",
                    "description": "Website is not using HTTPS (insecure connection)",
                    "severity": "high"
                })
            
            # Check for common vulnerabilities in response
            response_text = response.text.lower()
            if 'error' in response_text and ('sql' in response_text or 'database' in response_text):
                self.test_results.append({
                    "type": "security_vulnerability",
                    "category": "information_disclosure",
                    "description": "Potential database error information disclosure",
                    "severity": "high"
                })
                
        except Exception as e:
            self.test_results.append({
                "type": "error",
                "category": "security",
                "description": f"Security scan failed: {str(e)}",
                "severity": "medium"
            })
    
    def accessibility_audit(self):
        """Conduct accessibility audit"""
        print("♿ Conducting accessibility audit...")
        
        try:
            response = requests.get(self.base_url, timeout=30)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check for alt text on images
            images = soup.find_all('img')
            images_without_alt = [img for img in images if not img.get('alt')]
            
            if images_without_alt:
                self.test_results.append({
                    "type": "accessibility_issue",
                    "category": "missing_alt_text",
                    "description": f"Found {len(images_without_alt)} images without alt text",
                    "severity": "medium"
                })
            
            # Check for proper heading structure
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            heading_levels = [int(h.name[1]) for h in headings]
            
            # Check for skipped heading levels
            for i in range(len(heading_levels) - 1):
                if heading_levels[i+1] - heading_levels[i] > 1:
                    self.test_results.append({
                        "type": "accessibility_issue",
                        "category": "heading_structure",
                        "description": "Skipped heading levels detected (poor document structure)",
                        "severity": "low"
                    })
                    break
            
            # Check for form labels
            forms = soup.find_all('form')
            for form in forms:
                inputs = form.find_all('input')
                for input_field in inputs:
                    if input_field.get('type') not in ['submit', 'button', 'hidden']:
                        input_id = input_field.get('id')
                        if input_id:
                            label = soup.find('label', {'for': input_id})
                            if not label:
                                self.test_results.append({
                                    "type": "accessibility_issue",
                                    "category": "missing_labels",
                                    "description": f"Input field with id '{input_id}' lacks proper label",
                                    "severity": "medium"
                                })
            
            # Check for ARIA attributes
            elements_with_aria = soup.find_all(attrs={'aria-label': True}) + soup.find_all(attrs={'aria-labelledby': True})
            if not elements_with_aria:
                self.test_results.append({
                    "type": "accessibility_issue",
                    "category": "aria_attributes",
                    "description": "No ARIA attributes found (may affect screen reader accessibility)",
                    "severity": "low"
                })
                
        except Exception as e:
            self.test_results.append({
                "type": "error",
                "category": "accessibility",
                "description": f"Accessibility audit failed: {str(e)}",
                "severity": "medium"
            })
    
    def test_responsiveness(self):
        """Test website responsiveness"""
        print("📱 Testing responsiveness...")
        
        try:
            # Test with different user agents
            user_agents = {
                'desktop': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'mobile': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
                'tablet': 'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
            }
            
            for device, user_agent in user_agents.items():
                try:
                    headers = {'User-Agent': user_agent}
                    response = requests.get(self.base_url, headers=headers, timeout=30)
                    
                    if response.status_code == 200:
                        print(f"✅ {device.capitalize()} view: OK")
                    else:
                        self.test_results.append({
                            "type": "responsiveness_issue",
                            "category": "device_compatibility",
                            "description": f"Website not responding properly for {device} view (Status: {response.status_code})",
                            "severity": "medium"
                        })
                        
                except Exception as e:
                    self.test_results.append({
                        "type": "responsiveness_issue",
                        "category": "device_compatibility",
                        "description": f"Failed to test {device} responsiveness: {str(e)}",
                        "severity": "medium"
                    })
                    
        except Exception as e:
            self.test_results.append({
                "type": "error",
                "category": "responsiveness",
                "description": f"Responsiveness testing failed: {str(e)}",
                "severity": "medium"
            })
    
    def test_api_security(self):
        """Test API endpoint security"""
        print("🔌 Testing API security...")
        
        try:
            # Test with malformed data
            malformed_data = {
                "content": "<script>alert('XSS')</script>",
                "invalid_field": "test"
            }
            
            headers = {
                'Content-Type': 'application/json',
                'Origin': 'http://localhost:3000'
            }
            
            response = requests.post(API_ENDPOINT, json=malformed_data, headers=headers, timeout=30)
            
            # Check if API properly handles malformed input
            if response.status_code == 400:
                print("✅ API properly rejects malformed input")
            elif response.status_code == 200:
                # Check if XSS content is sanitized
                try:
                    result = response.json()
                    if "<script>" in str(result):
                        self.test_results.append({
                            "type": "security_vulnerability",
                            "category": "xss",
                            "description": "API may be vulnerable to XSS attacks (script tags not sanitized)",
                            "severity": "high"
                        })
                except:
                    pass
            else:
                self.test_results.append({
                    "type": "security_vulnerability",
                    "category": "input_validation",
                    "description": f"API returned unexpected status code for malformed input: {response.status_code}",
                    "severity": "medium"
                })
                
        except requests.exceptions.ConnectionError:
            print("⚠️ API endpoint not accessible for security testing")
        except Exception as e:
            self.test_results.append({
                "type": "error",
                "category": "api_security",
                "description": f"API security testing failed: {str(e)}",
                "severity": "medium"
            })
    
    def run_non_functional_tests(self):
        """Run all non-functional tests"""
        print("🚀 Starting Non-Functional Testing...")
        
        self.measure_performance()
        self.security_scan()
        self.accessibility_audit()
        self.test_responsiveness()
        self.test_api_security()
        
        print(f"✅ Non-functional testing completed. Found {len(self.test_results)} issues.")
        return self.test_results 