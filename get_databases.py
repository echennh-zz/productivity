import os
import requests

NOTION_API_KEY = os.getenv('NOTION_API_KEY')

headers = {
    'Authorization': f"Bearer {NOTION_API_KEY}",
    'Notion-Version': '2021-08-16',
}

response = requests.get('https://api.notion.com/v1/databases', headers=headers)