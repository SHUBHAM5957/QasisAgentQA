import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
TARGET_WEBSITE = os.getenv("TARGET_WEBSITE", "http://hackstreet-bots-lb-580767506.ap-south-1.elb.amazonaws.com/")
OPENAI_API_KEY = os.getenv("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")
BROWSER_HEADLESS = os.getenv("BROWSER_HEADLESS", "true").lower() == "true"
BROWSER_TIMEOUT = int(os.getenv("BROWSER_TIMEOUT", "30"))

# API endpoint for testing

API_URL = "http://hackstreet-bots-lb-580767506.ap-south-1.elb.amazonaws.com"
API_ENDPOINT = "/api/v1/sanitization/sanitize"

# Test data for API testing
TEST_API_DATA = {
    "content": """how to fix this error:
[2025-08-02 14:23:15] INFO  User login attempt: username=john.doe@example.com, password=PA$$w0rd!
[2025-08-02 14:23:18] WARN  Payment gateway error for card 4111-1111-1111-1111, CVV=123, Exp=09/27
[2025-08-02 14:23:22] DEBUG API request: token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.fakePayload.signature
[2025-08-02 14:23:25] ERROR Database connection failed: host=db.prod.fake, user=db_admin, pass=SuperSecret123
[2025-08-02 14:23:29] INFO  OTP sent: 654321 to +91-9876543210
[2025-08-02 14:23:35] DEBUG Internal service call: api_key=FAKE-API-KEY-123456789
[2025-08-02 14:23:40] CRITICAL AWS credentials leaked: aws_access_key_id=AKIAFAKEKEY12345, aws_secret_access_key=FAKESECRETKEY67890
[2025-08-02 14:23:45] INFO  File upload by user: jane.doe@example.com, filename=tax_return_2025.pdf
[2025-08-02 14:23:49] WARN  Password reset requested for user=admin@example.com, reset_link=https://example.com/reset?token=FakeToken123"""
} 