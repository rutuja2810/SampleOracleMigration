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

os.makedirs("exported_reports", exist_ok=True)

# Export report layout (.xdo)
report_path = "/Custom/Financials/Reports/MyReport.xdo"
print(f"Exporting report layout: {report_path}")
report_data = service.getReportDefinition(reportAbsolutePath=report_path)
with open("exported_reports/MyReport.xdo", "wb") as f:
    f.write(report_data)

# Export data model (.xdm)
data_model_path = "/Custom/Financials/Reports/MyDataModel.xdm"
print(f"Exporting data model: {data_model_path}")
data_model_data = service.downloadDataModel(dataModelAbsolutePath=data_model_path)
with open("exported_reports/MyDataModel.xdm", "wb") as f:
    f.write(data_model_data)
