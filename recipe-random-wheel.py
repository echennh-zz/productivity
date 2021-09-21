import os
import requests
import json

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
database_id = '361b30b6d9474262889bbe2c6c222ed8'

headers = {
    'Authorization': f"Bearer {NOTION_API_KEY}",
    'Notion-Version': '2021-08-16',
    'Content-Type': 'application/json',
}


response = requests.post(f'https://api.notion.com/v1/databases/{database_id}/query', headers=headers)

response_json = response.json()
print(json.dumps(response_json, indent=4))
returned_recipes = response_json.get('results')
