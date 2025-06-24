import argparse
import logging.config
import os
import requests
from zeep import Client
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
from zeep.exceptions import XMLSyntaxError

# Enable Zeep debug logging (optional)
logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'verbose': {'format': '%(name)s: %(message)s'}
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'zeep': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
        }
    }
})

# Parse CLI args
parser = argparse.ArgumentParser()
parser.add_argument('--url', required=True, help="Full WSDL URL (e.g., https://host/xmlpserver/services/PublicReportService?wsdl)")
parser.add_argument('--username', required=True)
parser.add_argument('--password', required=True)
args = parser.parse_args()

# Set up HTTP session with Basic Auth
session = requests.Session()
session.auth = HTTPBasicAuth(args.username, args.password)

# ✅ PRE-VALIDATE WSDL BEFORE PASSING TO Zeep
response = session.get(args.url)
content_type = response.headers.get("Content-Type", "")
if not response.ok:
    print(f"❌ Failed to fetch WSDL. Status code: {response.status_code}")
    print(response.text[:500])
    exit(1)

if "html" in content_type.lower():
    print("❌ Error: WSDL URL responded with HTML. This likely means:")
    print("   - The WSDL URL is incorrect")
    print("   - Authentication failed and returned a login page")
    print("   - Oracle SSO or WebGate is intercepting the request")
    print("Preview of response:")
    print(response.text[:500])
    exit(1)

# ✅ Continue with Zeep client
try:
    client = Client(wsdl=args.url, transport=Transport(session=session))
except XMLSyntaxError as e:
    print(f"❌ XML parsing failed. Is the URL pointing to a real WSDL? {e}")
    exit(1)

# 📦 Folder to store reports
EXPORT_FOLDER = "exported_reports"
os.makedirs(EXPORT_FOLDER, exist_ok=True)

# ❗️Placeholder logic: Replace with your real export call
report_path = "/Your/Report/Path.xdo"  # Update this!

try:
    print(f"Exporting report from: {report_path}")
    result = client.service.getDocumentData(report_path, '', False, '', '', '')
    output_path = os.path.join(EXPORT_FOLDER, os.path.basename(report_path))
    with open(output_path, "wb") as f:
        f.write(result)
    print(f"✅ Exported to: {output_path}")
except Exception as e:
    print(f"❌ Error exporting report: {e}")
    exit(1)
