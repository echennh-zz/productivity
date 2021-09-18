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

data = '{ "filter": { "and": [ { "property": "Status", "checkbox": { "equals": true } }, { "or": [ { "property": "Timeframe/how often", "multi_select": { "contains": "Once" } },{ "property": "Timeframe/how often", "multi_select": { "contains": "Annually" } } ] } ] } }'

response = requests.post('https://api.notion.com/v1/databases/cab6c589038043fcb63eda33fb5034d5/query', headers=headers, data=data)

response_json = response.json()
print(json.dumps(response_json, indent=4))
returned_tasks = response_json.get('results')
for task in returned_tasks:


# move the Tasks to the Archived Tasks database
