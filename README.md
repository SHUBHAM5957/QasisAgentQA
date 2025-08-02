# Website Testing QA Application

A comprehensive quality assurance testing system for websites that performs both functional and non-functional testing using specialized testers.

## 🎯 Overview

This application provides automated website testing capabilities with two specialized testers:

1. **FunctionalTester**: Expert in software quality assurance, responsible for verifying all functional aspects of websites
2. **NonFunctionalTester**: Specialist in performance, security, and accessibility testing

## 🚀 Features

### Functional Testing
- Website navigation verification
- Clickable elements testing (links, buttons, navigation)
- Form inspection and submission testing
- User flow verification
- API endpoint testing
- Bug documentation and reporting

### Non-Functional Testing
- Performance measurement (load time, response time, page size)
- Security scanning (headers, HTTPS, vulnerabilities)
- Accessibility auditing (alt text, headings, labels, ARIA)
- Responsiveness testing (desktop, mobile, tablet)
- API security testing

### Reporting
- Comprehensive JSON report generation
- Issue categorization by severity and type
- Actionable recommendations
- Summary statistics

## 📋 Requirements

- Python 3.8 or higher
- Chrome browser (for Selenium testing)
- Internet connection

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root with:
   ```
   TARGET_WEBSITE=http://52.66.221.29:3000/
   OPENAI_API_KEY=your_openai_api_key_here
   BROWSER_HEADLESS=true
   BROWSER_TIMEOUT=30
   ```

## 🚀 Usage

### Basic Usage
```bash
python main.py
```

### What the application does:

1. **Initializes both testers**
2. **Runs functional tests:**
   - Navigates to the target website
   - Tests all clickable elements
   - Validates forms and user flows
   - Tests API endpoints

3. **Runs non-functional tests:**
   - Measures performance metrics
   - Performs security scans
   - Conducts accessibility audits
   - Tests responsiveness
   - Validates API security

4. **Generates comprehensive report:**
   - Combines all findings
   - Categorizes issues by severity
   - Provides actionable recommendations
   - Saves detailed JSON report

## 📊 Output

The application provides:

1. **Real-time console output** showing test progress
2. **Comprehensive summary** with issue counts and severity levels
3. **Detailed JSON report** saved to file with timestamp
4. **Exit codes** indicating overall test status:
   - `0`: All tests passed
   - `1`: Critical issues found
   - `2`: High priority issues found
   - `3`: Medium/low issues found

## 🔧 Configuration

### Target Website
Edit `config.py` or set environment variable:
```python
TARGET_WEBSITE = "http://your-website.com/"
```

### API Testing
The application includes testing for the sanitize API endpoint:
```python
API_ENDPOINT = "http://localhost:8080/api/sanitize"
```

### Test Data
The application uses predefined test data for API testing, including:
- Log entries with sensitive information
- Database connection strings
- API keys and tokens
- Payment information

## 📁 Project Structure

```
QAAGENT/
├── main.py                 # Main application entry point
├── config.py              # Configuration settings
├── functional_tester.py   # Functional testing implementation
├── non_functional_tester.py # Non-functional testing implementation
├── report_generator.py    # Report generation and formatting
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🧪 Testing Features

### Functional Testing
- **Navigation Testing**: Verifies website loads correctly
- **Element Testing**: Tests all clickable elements (links, buttons, forms)
- **Form Validation**: Checks required fields and validation messages
- **API Testing**: Tests the sanitize API endpoint with sensitive data

### Non-Functional Testing
- **Performance**: Load time, response time, page size analysis
- **Security**: Headers, HTTPS, XSS protection, input validation
- **Accessibility**: Alt text, heading structure, form labels, ARIA attributes
- **Responsiveness**: Cross-device compatibility testing

## 🔍 Sample Output

```
🚀 Website Testing QA Application
==================================================
Target Website: http://52.66.221.29:3000/
Test Date: 2024-01-15 10:30:00
==================================================

✅ All required dependencies are available

🔧 Initializing testers...

==================================================
🔍 FUNCTIONAL TESTING
==================================================
🚀 Starting Functional Testing...
🌐 Navigating to: http://52.66.221.29:3000/
✅ Successfully loaded: Website Title
🔍 Testing clickable elements...
✅ Link: 'Home' - Navigation successful
✅ Button: 'Submit' - Click successful
📝 Testing forms...
🔍 Testing form: contact-form
✅ Form validation working for email
🔌 Testing API endpoint...
✅ API endpoint responded successfully

==================================================
🔍 NON-FUNCTIONAL TESTING
==================================================
🚀 Starting Non-Functional Testing...
⚡ Measuring performance...
📊 Performance Metrics:
   - Load Time: 1.23 seconds
   - Response Time: 0.45 seconds
   - Page Size: 245.67 KB
🔒 Performing security scan...
♿ Conducting accessibility audit...
📱 Testing responsiveness...
✅ Desktop view: OK
✅ Mobile view: OK
✅ Tablet view: OK
🔌 Testing API security...
✅ API properly rejects malformed input

==================================================
📋 GENERATING REPORT
==================================================
📊 Processing functional testing results...
📊 Processing non-functional testing results...
💡 Generating recommendations...

================================================================================
🔍 COMPREHENSIVE QA TESTING REPORT
================================================================================

📊 SUMMARY:
   Target Website: http://52.66.221.29:3000/
   Test Date: 2024-01-15T10:30:00
   Total Issues Found: 3
   Critical Issues: 0
   High Issues: 1
   Medium Issues: 2
   Low Issues: 0

⚠️  3 issues found that need attention.

🚨 CRITICAL & HIGH PRIORITY ISSUES (1):
   1. [HIGH] https: Website is not using HTTPS (insecure connection)

💡 RECOMMENDATIONS:
   • Security (high priority): Implement security headers and HTTPS to protect against common vulnerabilities
   • Performance (medium priority): Optimize website performance for better user experience

✅ Report saved to: qa_report_20240115_103000.json
```

## 🐛 Troubleshooting

### Common Issues

1. **Chrome Driver Issues**
   - The application automatically downloads ChromeDriver
   - Ensure Chrome browser is installed
   - Check internet connection for driver download

2. **Website Not Accessible**
   - Verify the target website URL is correct
   - Check if the website is running and accessible
   - Ensure proper network connectivity

3. **API Endpoint Issues**
   - Verify the API endpoint is running on localhost:8080
   - Check if the API accepts the test data format
   - Ensure CORS is properly configured

### Error Codes
- **Exit 1**: Critical issues found
- **Exit 2**: High priority issues found  
- **Exit 3**: Medium/low issues found
- **Exit 0**: All tests passed

## 🤝 Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the error messages in the console output
3. Check the generated JSON report for detailed information
4. Ensure all dependencies are properly installed 