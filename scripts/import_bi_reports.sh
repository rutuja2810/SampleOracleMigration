#!/bin/bash

# Usage:
# ./import_bi_report.sh <BASE_URL> <USERNAME> <PASSWORD>
# Example:
# ./import_bi_report.sh https://host:port/xmlpserver myuser mypassword

# Assign command-line args to variables
BASE_URL="$1"      # e.g., https://host:port/xmlpserver
USERNAME="$2"      # e.g., myuser
PASSWORD="$3"      # e.g., mypassword

WSDL_URL="${BASE_URL}/services/PublicReportService?wsdl"

# Export folder for reports (make sure it exists)
EXPORT_FOLDER="exported_reports"

# Example report details: filename and report path in BI server
declare -a FILES=("MyReport.xdo" "MyDataModel.xdm")
declare -a PATHS=("/Custom/Financials/Reports/MyReport.xdo" "/Custom/Financials/Reports/MyDataModel.xdm")

# Loop through each file and upload
for i in "${!FILES[@]}"; do
  FILE="${FILES[$i]}"
  REPORT_PATH="${PATHS[$i]}"

  # Check if file exists
  if [[ ! -f "${EXPORT_FOLDER}/${FILE}" ]]; then
    echo "File ${EXPORT_FOLDER}/${FILE} not found!"
    exit 1
  fi

  echo "Importing ${FILE} to ${REPORT_PATH}..."

  # Use curl to upload report (adjust endpoint and payload as needed)
  curl -u "${USERNAME}:${PASSWORD}" \
    -X POST \
    -H "Content-Type: application/octet-stream" \
    --data-binary @"${EXPORT_FOLDER}/${FILE}" \
    "${BASE_URL}/services/PublicReportService/uploadReport?reportPath=${REPORT_PATH}"

  echo "Imported: ${FILE}"
done
