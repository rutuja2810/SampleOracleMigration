import argparse, os
from zeep import Client
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport
import requests

parser = argparse.ArgumentParser()
parser.add_argument('--url', required=True)
parser.add_argument('--username', required=True)
parser.add_argument('--password', required=True)
args = parser.parse_args()

wsdl = f"{args.url}/xmlpserver/services/PublicReportService?wsdl"
session = requests.Session()
session.auth = HTTPBasicAuth(args.username, args.password)
client = Client(wsdl, transport=Transport(session=session))
service = client.service

# Define the list of report paths to export
report_paths = [
    "/Custom/Financials/Reports/MyReport.xdo",
    "/Custom/Financials/Reports/MyDataModel.xdm"
]

os.makedirs("exported_reports", exist_ok=True)

for path in report_paths:
    filename = os.path.basename(path)
    print(f"Exporting: {filename}")
    content = service.downloadReport(path)
    with open(f"exported_reports/{filename}", "wb") as f:
        f.write(content)
