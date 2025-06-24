#!/bin/bash

# Usage:
# ./export_report.sh --url "https://host/xmlpserver/services/PublicReportService" --username USER --password PASS --report_path "/Custom/Financials/Reports/MyReport.xdo"

while [[ $# -gt 0 ]]; do
  case $1 in
    --url)
      URL="$2"
      shift 2
      ;;
    --username)
      USERNAME="$2"
      shift 2
      ;;
    --password)
      PASSWORD="$2"
      shift 2
      ;;
    --report_path)
      REPORT_PATH="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$URL" || -z "$USERNAME" || -z "$PASSWORD" || -z "$REPORT_PATH" ]]; then
  echo "Missing required parameters."
  echo "Usage: $0 --url URL --username USERNAME --password PASSWORD --report_path REPORT_PATH"
  exit 1
fi

SOAP_BODY="<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"
                  xmlns:pub=\"http://xmlns.oracle.com/oxp/service/PublicReportService\">
   <soapenv:Header/>
   <soapenv:Body>
      <pub:getDocumentData>
         <pub:reportRequest>
            <pub:reportAbsolutePath>${REPORT_PATH}</pub:reportAbsolutePath>
            <pub:sizeOfDataChunkDownload>-1</pub:sizeOfDataChunkDownload>
         </pub:reportRequest>
      </pub:getDocumentData>
   </soapenv:Body>
</soapenv:Envelope>"

echo "Requesting report ${REPORT_PATH} from ${URL}..."

curl -s --fail -u "$USERNAME:$PASSWORD" \
  -H "Content-Type: text/xml;charset=UTF-8" \
  -H "SOAPAction: getDocumentData" \
  -d "$SOAP_BODY" \
  "$URL" -o exported_report.xml

if [[ $? -eq 0 ]]; then
  echo "✅ Report saved to exported_report.xml"
else
  echo "❌ Failed to fetch report."
fi
