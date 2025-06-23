import argparse
import os
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

items = [
    ("MyReport.xdo", "/Custom/Financials/Reports/MyReport.xdo"),
    ("MyDataModel.xdm", "/Custom/Financials/Reports/MyDataModel.xdm")
]

for file_name, report_path in items:
    with open(f"exported_reports/{file_name}", "rb") as f:
        data = f.read()

    print(f"Importing {file_name} to {report_path}")

    service.uploadReport(
        reportPath=report_path,
        reportData=data,
        userID=args.username
    )
    print(f"Imported: {file_name}")
