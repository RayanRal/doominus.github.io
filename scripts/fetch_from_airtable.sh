#!/bin/bash

DATA_FILE=../_data/numbers.json
API_KEY=$AIRTABLE_API_KEY  # fetch from github secrets in action
BASE_ID=app7FmZOctdBwZwkZ
TABLE_ID=tblzr7cSMyyhdLuBD
REQUEST_DATE=$(date -v-1d +'%Y-%m-%d')
echo "$REQUEST_DATE"

AIRTABLE_URL="https://api.airtable.com/v0/$BASE_ID/$TABLE_ID?filterByFormula=DATESTR(%7BDate%7D)%3D'$REQUEST_DATE'"
AIRTABLE_HEADER="Authorization: Bearer $API_KEY"

# Clear the file
echo -n "" >$DATA_FILE

# Query Airtable
DATA_JSON=$(curl -H "$AIRTABLE_HEADER" "$AIRTABLE_URL") 

# Save result to file
echo "$DATA_JSON" | jq >>$DATA_FILE
date >last_updated_date
