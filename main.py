#!/usr/bin/env python3
"""
Website Testing QA Application
Comprehensive quality assurance testing for websites using specialized testers
"""

import sys
import os
from functional_tester import FunctionalTester
from non_functional_tester import NonFunctionalTester
from report_generator import ReportGenerator
from config import TARGET_WEBSITE, OPENAI_API_KEY

def main():
    """Main function to run the website testing QA application"""
    
    print("🚀 Website Testing QA Application")
    print("="*50)
    print(f"Target Website: {TARGET_WEBSITE}")
    print(f"Test Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    # Check if we have the required dependencies
    try:
        import requests
        import selenium
        import bs4
        print("✅ All required dependencies are available")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install required packages: pip install -r requirements.txt")
        sys.exit(1)
    
    # Initialize testers
    print("\n🔧 Initializing testers...")
    functional_tester = FunctionalTester()
    non_functional_tester = NonFunctionalTester()
    report_generator = ReportGenerator()
    
    # Run functional tests
    print("\n" + "="*50)
    print("🔍 FUNCTIONAL TESTING")
    print("="*50)
    functional_results = functional_tester.run_functional_tests()
    
    # Run non-functional tests
    print("\n" + "="*50)
    print("🔍 NON-FUNCTIONAL TESTING")
    print("="*50)
    non_functional_results = non_functional_tester.run_non_functional_tests()
    
    # Generate comprehensive report
    print("\n" + "="*50)
    print("📋 GENERATING REPORT")
    print("="*50)
    
    report = report_generator.generate_report(functional_results, non_functional_results)
    
    # Print summary
    report_generator.print_summary(report)
    
    # Save report to file
    report_filename = report_generator.save_report(report)
    
    if report_filename:
        print(f"\n📄 Detailed report saved to: {report_filename}")
        print("You can open this file to view the complete testing results and recommendations.")
    
    # Exit with appropriate code
    if report["summary"]["critical_issues"] > 0:
        print("\n❌ Critical issues found. Website requires immediate attention.")
        sys.exit(1)
    elif report["summary"]["high_issues"] > 0:
        print("\n⚠️  High priority issues found. Website needs improvement.")
        sys.exit(2)
    elif report["summary"]["total_issues"] > 0:
        print("\n⚠️  Issues found. Consider addressing them for better quality.")
        sys.exit(3)
    else:
        print("\n🎉 All tests passed! Website quality is excellent.")
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Testing interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1) 