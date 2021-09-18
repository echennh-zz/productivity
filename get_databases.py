import os
import requests
import json

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
database_id = 'cab6c589038043fcb63eda33fb5034d5'

headers = {
    'Authorization': f"Bearer {NOTION_API_KEY}",
    'Notion-Version': '2021-08-16',
    'Content-Type': 'application/json',
}

data = '{ "filter": { "and": [ { "property": "Status", "checkbox": { "equals": true } }, { "property": "Timeframe/how often", "multi_select": { "contains": "Once" } } ] }, "sorts": [ { "property": "Last Updated", "direction": "ascending" } ] }'

response = requests.post('https://api.notion.com/v1/databases/cab6c589038043fcb63eda33fb5034d5/query', headers=headers, data=data)

response_json = response.json()
print(json.dumps(response_json, indent=4))