import todoist # need to install todoist-python
import os
# also need to install notion-client

# You need the title of your Notion Dashboard to be "Task"
# You need a date column of your Notion Dashboard to be "Date"
# You need a multi-select column of your Notion Dashboard to be "Dashboard" and should have already created the "ToDoIst" option on Notion
# ALL OF THE VALUES YOU PASTE HERE SHOULD BE IN STRINGS
TODOIST_API_KEY = os.environ['TODOIST_API_KEY']  #copy and paste the api key
TODOIST_label_id = '2157876807' #when you're on the website and under the specific label, you'll be able to get the id by inspect element and finding the number
NOTION_API_KEY = os.environ['NOTION_API_KEY']    #  "secret_somneklhjslkdgjsdljfg" or something like that
# Don't forget to share your database with your Todoist to Notion Integration. Go to the db in Notion, click Share, then select the integration.
database_id = 'cab6c589038043fcb63eda33fb5034d5' #get the mess of numbers and letters before the "?" on your dashboard URL

api = todoist.TodoistAPI(TODOIST_API_KEY)
api.sync()

import requests

resultList=requests.get(
    "https://api.todoist.com/rest/v1/tasks",
    # params={
    #     "label_id": TODOIST_label_id
    # },
    headers={
        "Authorization": "Bearer %s" % TODOIST_API_KEY
    }).json()


taskData = []

import os
from notion_client import Client
from pprint import pprint
from datetime import datetime

os.environ['NOTION_TOKEN'] = NOTION_API_KEY
notion = Client(auth=os.environ["NOTION_TOKEN"])

for result in resultList:
    print(result)
    print("\n")

    taskName = result['content']
    dueDate = result.get('due')
    if dueDate:
        dueDate = dueDate.get('date')

    parent = {"database_id": database_id}
    task_prop = {
                        "type": 'title',
                        "title": [
                            {
                                "type": 'text',
                                "text": {
                                    "content": taskName,
                                },
                            },
                        ],
                    }

    date_prop = {"type": 'date',
                        'date': {
                            'start': dueDate,
                            'end': None,
                        }
                    }

    # dashboard_prop = {
    #                     "type": 'multi_select',
    #                     'multi_select': [{
    #                         "name": "ToDoIst"
    #                     }],
    #                 }

    if dueDate: # if there is a date:
        properties = {"Task": task_prop, "Due Date": date_prop}
    else:
        properties = {"Task": task_prop}


    notion_page_to_create = {"parent": parent, "properties": properties}

    #Enter the task into Notion
    my_page = notion.pages.create(
        **notion_page_to_create
    )

    #Delete the task from ToDoIst (the api stuff is defined in the first 3 lines of the program)

    item = api.items.get_by_id(result['id'])
    item.delete()
    api.commit()