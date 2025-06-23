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

# Construct WSDL and SOAP client
wsdl = f"{args.url}/xmlpserver/services/PublicReportService?wsdl"
session = requests.Session()
session.auth = HTTPBasicAuth(args.username, args.password)
client = Client(wsdl, transport=Transport(session=session))
service = client.service

# Define report and data model paths
reports = [
    ("MyReport.xdo", "/Custom/Financials/Reports/MyReport.xdo", "report"),     # layout
    ("MyDataModel.xdm", "/Custom/Financials/Reports/MyDataModel.xdm", "datamodel")  # data model
]

output_dir = "exported_reports"
os.makedirs(output_dir, exist_ok=True)

for file_name, path, type in reports:
    print(f"Exporting: {file_name}")

    if type == "report":
        result = service.getReportDefinition(reportAbsolutePath=path)
    elif type == "datamodel":
        result = service.downloadDataModel(dataModelAbsolutePath=path)
    else:
        print(f"Unknown type: {type}")
        continue

    with open(os.path.join(output_dir, file_name), "wb") as f:
        f.write(result)
