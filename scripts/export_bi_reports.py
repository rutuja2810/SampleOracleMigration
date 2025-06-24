import argparse
import logging.config
import os
import requests
from zeep import Client
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth

# Optional: Enable Zeep debug logging
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

# Parse CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('--url', required=True, help="Full WSDL URL (e.g., https://host/xmlpserver/services/PublicReportService?wsdl)")
parser.add_argument('--username', required=True)
parser.add_argument('--password', required=True)
args = parser.parse_args()

# Set up authenticated session
session = requests.Session()
session.auth = HTTPBasicAuth(args.username, args.password)

# Create Zeep SOAP client
client = Client(wsdl=args.url, transport=Transport(session=session))

# Export logic (simplified)
EXPORT_FOLDER = "exported_reports"
os.makedirs(EXPORT_FOLDER, exist_ok=True)

# Example: list a report and download it (update this logic as needed)
# Replace '/Your/Report/Path.xdo' with the actual path
report_path = "/Your/Report/Path.xdo"

try:
    print(f"Exporting report from: {report_path}")
    result = client.service.getDocumentData(report_path, '', False, '', '', '')
    
    output_path = os.path.join(EXPORT_FOLDER, os.path.basename(report_path))
    with open(output_path, "wb") as f:
        f.write(result)
    
    print(f"Exported to: {output_path}")

except Exception as e:
    print(f"Error exporting report: {e}")
