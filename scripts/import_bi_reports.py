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

# Same paths as used in export
items = [
    ("MyReport.xdo", "/Custom/Financials/Reports/MyReport.xdo"),
    ("MyDataModel.xdm", "/Custom/Financials/Reports/MyDataModel.xdm")
]

for file, path in items:
    with open(f"exported_reports/{file}", "rb") as f:
        data = f.read()
        service.uploadReport(reportPath=path, reportData=data)
        print(f"Imported: {file}")
