import json
from datetime import datetime
from typing import List, Dict, Any
from config import TARGET_WEBSITE

class ReportGenerator:
    def __init__(self):
        self.report = {
            "test_info": {
                "target_website": TARGET_WEBSITE,
                "test_date": datetime.now().isoformat(),
                "test_type": "Comprehensive QA Testing"
            },
            "summary": {
                "total_issues": 0,
                "critical_issues": 0,
                "high_issues": 0,
                "medium_issues": 0,
                "low_issues": 0
            },
            "issues": [],
            "recommendations": []
        }
    
    def add_functional_results(self, functional_results: List[Dict[str, Any]]):
        """Add functional testing results to the report"""
        print("📊 Processing functional testing results...")
        
        for issue in functional_results:
            self.report["issues"].append({
                **issue,
                "tester": "FunctionalTester",
                "test_category": "functional"
            })
    
    def add_non_functional_results(self, non_functional_results: List[Dict[str, Any]]):
        """Add non-functional testing results to the report"""
        print("📊 Processing non-functional testing results...")
        
        for issue in non_functional_results:
            self.report["issues"].append({
                **issue,
                "tester": "NonFunctionalTester",
                "test_category": "non_functional"
            })
    
    def generate_summary(self):
        """Generate summary statistics"""
        total_issues = len(self.report["issues"])
        critical_issues = len([i for i in self.report["issues"] if i["severity"] == "critical"])
        high_issues = len([i for i in self.report["issues"] if i["severity"] == "high"])
        medium_issues = len([i for i in self.report["issues"] if i["severity"] == "medium"])
        low_issues = len([i for i in self.report["issues"] if i["severity"] == "low"])
        
        self.report["summary"] = {
            "total_issues": total_issues,
            "critical_issues": critical_issues,
            "high_issues": high_issues,
            "medium_issues": medium_issues,
            "low_issues": low_issues
        }
    
    def generate_recommendations(self):
        """Generate recommendations based on findings"""
        print("💡 Generating recommendations...")
        
        recommendations = []
        
        # Analyze issues by category
        security_issues = [i for i in self.report["issues"] if "security" in i["category"]]
        performance_issues = [i for i in self.report["issues"] if "performance" in i["category"]]
        accessibility_issues = [i for i in self.report["issues"] if "accessibility" in i["category"]]
        functional_issues = [i for i in self.report["issues"] if i["test_category"] == "functional"]
        
        # Security recommendations
        if security_issues:
            recommendations.append({
                "category": "Security",
                "priority": "high",
                "description": "Implement security headers and HTTPS to protect against common vulnerabilities",
                "actions": [
                    "Add X-Frame-Options, X-Content-Type-Options, and X-XSS-Protection headers",
                    "Implement HTTPS with proper SSL/TLS configuration",
                    "Add Content Security Policy (CSP) headers",
                    "Implement input validation and sanitization for all user inputs"
                ]
            })
        
        # Performance recommendations
        if performance_issues:
            recommendations.append({
                "category": "Performance",
                "priority": "medium",
                "description": "Optimize website performance for better user experience",
                "actions": [
                    "Optimize images and assets to reduce page size",
                    "Implement caching strategies",
                    "Optimize server response times",
                    "Consider using a CDN for static assets"
                ]
            })
        
        # Accessibility recommendations
        if accessibility_issues:
            recommendations.append({
                "category": "Accessibility",
                "priority": "medium",
                "description": "Improve website accessibility for users with disabilities",
                "actions": [
                    "Add alt text to all images",
                    "Ensure proper heading structure (h1, h2, h3, etc.)",
                    "Add proper labels to form inputs",
                    "Implement ARIA attributes for better screen reader support"
                ]
            })
        
        # Functional recommendations
        if functional_issues:
            recommendations.append({
                "category": "Functionality",
                "priority": "high",
                "description": "Fix functional issues to ensure proper website operation",
                "actions": [
                    "Fix broken links and navigation issues",
                    "Implement proper form validation",
                    "Test all user flows thoroughly",
                    "Ensure API endpoints are working correctly"
                ]
            })
        
        # General recommendations
        if self.report["summary"]["total_issues"] > 0:
            recommendations.append({
                "category": "General",
                "priority": "medium",
                "description": "Implement comprehensive testing and monitoring",
                "actions": [
                    "Set up automated testing pipelines",
                    "Implement continuous monitoring for performance and security",
                    "Regular security audits and penetration testing",
                    "User acceptance testing with real users"
                ]
            })
        
        self.report["recommendations"] = recommendations
    
    def generate_report(self, functional_results: List[Dict[str, Any]], non_functional_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate the complete QA report"""
        print("📋 Generating comprehensive QA report...")
        
        self.add_functional_results(functional_results)
        self.add_non_functional_results(non_functional_results)
        self.generate_summary()
        self.generate_recommendations()
        
        return self.report
    
    def save_report(self, report: Dict[str, Any], filename: str = None):
        """Save the report to a JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qa_report_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"✅ Report saved to: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Failed to save report: {e}")
            return None
    
    def print_summary(self, report: Dict[str, Any]):
        """Print a summary of the report"""
        print("\n" + "="*80)
        print("🔍 COMPREHENSIVE QA TESTING REPORT")
        print("="*80)
        
        summary = report["summary"]
        print(f"\n📊 SUMMARY:")
        print(f"   Target Website: {report['test_info']['target_website']}")
        print(f"   Test Date: {report['test_info']['test_date']}")
        print(f"   Total Issues Found: {summary['total_issues']}")
        print(f"   Critical Issues: {summary['critical_issues']}")
        print(f"   High Issues: {summary['high_issues']}")
        print(f"   Medium Issues: {summary['medium_issues']}")
        print(f"   Low Issues: {summary['low_issues']}")
        
        if summary['total_issues'] == 0:
            print("\n🎉 EXCELLENT! No issues found during testing.")
        else:
            print(f"\n⚠️  {summary['total_issues']} issues found that need attention.")
            
            # Print critical and high issues first
            critical_high_issues = [i for i in report["issues"] if i["severity"] in ["critical", "high"]]
            if critical_high_issues:
                print(f"\n🚨 CRITICAL & HIGH PRIORITY ISSUES ({len(critical_high_issues)}):")
                for i, issue in enumerate(critical_high_issues, 1):
                    print(f"   {i}. [{issue['severity'].upper()}] {issue['category']}: {issue['description']}")
            
            # Print recommendations
            if report["recommendations"]:
                print(f"\n💡 RECOMMENDATIONS:")
                for rec in report["recommendations"]:
                    print(f"   • {rec['category']} ({rec['priority']} priority): {rec['description']}")
        
        print("\n" + "="*80) 