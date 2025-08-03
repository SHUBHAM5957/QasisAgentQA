import requests
import time
import json
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from config import TARGET_WEBSITE, API_URL, API_ENDPOINT, TEST_API_DATA

class NonFunctionalTester:
    def __init__(self):
        self.test_results = []
        self.base_url = TARGET_WEBSITE
        self.api_url = API_URL
        self.api_endpoint = f"{API_URL.rstrip('/')}/{API_ENDPOINT.lstrip('/')}"
        
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
            # Headers based on the curl command
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9,en-IN;q=0.8',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Origin': API_URL,
                'Referer': f"{API_URL}/"
            }
            
            print(f"Testing API endpoint: {self.api_endpoint}")
            
            # Test with malformed XSS data
            xss_data = {
                "content": "<script>alert('XSS')</script> - Testing XSS vulnerability in log sanitization"
            }
            
            try:
                response = requests.post(self.api_endpoint, json=xss_data, headers=headers, timeout=30)
                
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
                        else:
                            print("✅ API properly sanitizes XSS content")
                    except json.JSONDecodeError:
                        print("⚠️ API response is not valid JSON")
                else:
                    self.test_results.append({
                        "type": "security_vulnerability",
                        "category": "input_validation",
                        "description": f"API returned unexpected status code for malformed input: {response.status_code}",
                        "severity": "medium"
                    })
                    
            except requests.exceptions.RequestException as e:
                print(f"⚠️ XSS test failed: {str(e)}")
            
            # Test with the sample test data from config
            print("Testing with sample log data...")
            try:
                response = requests.post(self.api_endpoint, json=TEST_API_DATA, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    try:
                        result = response.json()
                        print("✅ API responded successfully to test data")
                        
                        # Check if sensitive data is properly sanitized
                        sensitive_patterns = ['password=', 'pass=', 'api_key=', 'token=', 'aws_access_key', 'aws_secret_access_key', 'CVV=', 'card ', 'OTP ']
                        found_sensitive = []
                        result_str = str(result).lower()
                        
                        for pattern in sensitive_patterns:
                            if pattern.lower() in result_str:
                                # Check if it's actually sanitized (masked/redacted)
                                if '*' in result_str or '[REDACTED]' in result_str or '[MASKED]' in result_str:
                                    continue  # It's properly sanitized
                                found_sensitive.append(pattern)
                        
                        if found_sensitive:
                            self.test_results.append({
                                "type": "security_vulnerability",
                                "category": "data_sanitization",
                                "description": f"API may not be properly sanitizing sensitive data patterns: {', '.join(found_sensitive)}",
                                "severity": "high"
                            })
                        else:
                            print("✅ API properly sanitizes sensitive data")
                            
                        # Check response structure
                        if isinstance(result, dict) and 'sanitized_content' in result:
                            print("✅ API returns expected response structure")
                        else:
                            print("⚠️ API response structure may be unexpected")
                            
                    except json.JSONDecodeError:
                        self.test_results.append({
                            "type": "error",
                            "category": "api_response",
                            "description": "API response is not valid JSON",
                            "severity": "medium"
                        })
                elif response.status_code == 400:
                    print("⚠️ API rejected test data with 400 status")
                elif response.status_code == 404:
                    self.test_results.append({
                        "type": "api_issue",
                        "category": "endpoint_not_found",
                        "description": f"API endpoint not found: {self.api_endpoint}",
                        "severity": "high"
                    })
                else:
                    self.test_results.append({
                        "type": "api_issue",
                        "category": "response_code",
                        "description": f"API returned status code {response.status_code} for test data",
                        "severity": "medium"
                    })
                    
            except requests.exceptions.RequestException as e:
                print(f"⚠️ Test data request failed: {str(e)}")
                
        except requests.exceptions.ConnectionError:
            print("⚠️ API endpoint not accessible for security testing")
            self.test_results.append({
                "type": "connectivity_issue",
                "category": "api_unreachable",
                "description": f"Cannot connect to API endpoint: {self.api_endpoint}",
                "severity": "high"
            })
        except Exception as e:
            self.test_results.append({
                "type": "error",
                "category": "api_security",
                "description": f"API security testing failed: {str(e)}",
                "severity": "medium"
            })
    
    def test_cors_policy(self):
        """Test CORS policy configuration"""
        print("🌐 Testing CORS policy...")
        
        try:
            # Test preflight request
            headers = {
                'Origin': 'http://hackstreet-bots-lb-580767506.ap-south-1.elb.amazonaws.com',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            }
            
            response = requests.options(self.api_endpoint, headers=headers, timeout=30)
            
            if 'Access-Control-Allow-Origin' in response.headers:
                allowed_origin = response.headers['Access-Control-Allow-Origin']
                if allowed_origin == '*':
                    self.test_results.append({
                        "type": "security_vulnerability",
                        "category": "cors_wildcard",
                        "description": "CORS policy allows all origins (*) - potential security risk",
                        "severity": "medium"
                    })
                else:
                    print(f"✅ CORS properly configured for origin: {allowed_origin}")
            else:
                self.test_results.append({
                    "type": "configuration_issue",
                    "category": "cors_missing",
                    "description": "CORS headers not found - may cause cross-origin request issues",
                    "severity": "low"
                })
                
        except Exception as e:
            print(f"⚠️ CORS testing failed: {str(e)}")
    
    def test_api_rate_limiting(self):
        """Test API rate limiting"""
        print("⏱️ Testing API rate limiting...")
        
        try:
            headers = {
                'Accept': '*/*',
                'Content-Type': 'application/json',
                'Origin': API_URL,
                'Referer': f"{API_URL}/"
            }
            
            simple_data = {"content": "test log entry"}
            
            # Send multiple requests quickly
            responses = []
            for i in range(10):
                try:
                    response = requests.post(self.api_endpoint, json=simple_data, headers=headers, timeout=10)
                    responses.append(response.status_code)
                except Exception:
                    responses.append(None)
                time.sleep(0.1)  # Small delay between requests
            
            # Check for rate limiting responses (429 status code)
            rate_limited = [r for r in responses if r == 429]
            if rate_limited:
                print(f"✅ API has rate limiting (received {len(rate_limited)} rate limit responses)")
            else:
                print("⚠️ No rate limiting detected - may allow abuse")
                self.test_results.append({
                    "type": "security_vulnerability",
                    "category": "rate_limiting",
                    "description": "API does not appear to implement rate limiting",
                    "severity": "medium"
                })
                
        except Exception as e:
            print(f"⚠️ Rate limiting test failed: {str(e)}")
    
    def run_non_functional_tests(self):
        """Run all non-functional tests"""
        print("🚀 Starting Non-Functional Testing...")
        print(f"Target Website: {self.base_url}")
        print(f"API Endpoint: {self.api_endpoint}")
        print("-" * 60)
        
        self.measure_performance()
        print("-" * 30)
        self.security_scan()
        print("-" * 30)
        self.accessibility_audit()
        print("-" * 30)
        self.test_responsiveness()
        print("-" * 30)
        self.test_api_security()
        print("-" * 30)
        self.test_cors_policy()
        print("-" * 30)
        self.test_api_rate_limiting()
        print("-" * 60)
        
        print(f"✅ Non-functional testing completed. Found {len(self.test_results)} issues.")
        
        # Print summary of issues by severity
        if self.test_results:
            severity_counts = {}
            for result in self.test_results:
                severity = result.get('severity', 'unknown')
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            print("\n📊 Issues Summary:")
            for severity, count in severity_counts.items():
                print(f"   - {severity.title()}: {count}")
        
        return self.test_results