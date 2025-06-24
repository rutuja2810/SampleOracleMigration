#!/bin/bash

# Parse arguments
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
    *)
      echo "Unknown option $1"
      exit 1
      ;;
  esac
done

if [[ -z "$URL" || -z "$USERNAME" || -z "$PASSWORD" ]]; then
  echo "Usage: $0 --url <WSDL or base BI URL> --username <username> --password <password>"
  exit 1
fi

# Folder to store exported reports
EXPORT_FOLDER="exported_reports"
mkdir -p "$EXPORT_FOLDER"

echo "✅ Verifying WSDL URL accessibility..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -u "$USERNAME:$PASSWORD" "$URL")

if [[ "$HTTP_CODE" -ne 200 ]]; then
  echo "❌ Failed to fetch WSDL. HTTP status: $HTTP_CODE"
  exit 1
fi

echo "✅ WSDL URL accessible."

# Define your report path relative to BI server, e.g. /Your/Report/Path.xdo
REPORT_PATH="/Your/Report/Path.xdo"

# Construct full export URL (adjust this based on your BI export endpoint)
# If URL is WSDL, remove '?wsdl' and append report path
BASE_URL="${URL%?wsdl}"

EXPORT_URL="${BASE_URL}${REPORT_PATH}"

echo "Exporting report from: $EXPORT_URL"

OUTPUT_FILE="$EXPORT_FOLDER/$(basename "$REPORT_PATH")"

curl -s -u "$USERNAME:$PASSWORD" -o "$OUTPUT_FILE" "$EXPORT_URL"

if [[ $? -eq 0 ]]; then
  echo "✅ Report exported successfully to $OUTPUT_FILE"
else
  echo "❌ Failed to export report"
fi
