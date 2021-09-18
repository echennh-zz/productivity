import todoist # need to install todoist-python
import os
import requests
# also need to install notion-client

# Text parsing begin #
import datetime
from recurrent.event_parser import RecurringEvent
r = RecurringEvent(now_date=datetime.date.today())

def parse_date_from_text(dueString):
    recurrent_str = r.parse(dueString)
    # I guess, I want to get the next 7 occurences to start, and I can expand upon this later
    # I can install python_dateutil, and feed it the rrules string recurrent_str, and get the next dates
    return recurrent_str

# Text parsing end #

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
    dueBlock = result.get('due')
    if dueBlock:
        dueDate = dueBlock.get('date')
        recur = dueBlock.get('recurring')
        if recur:
            print(f"due date string from todoist: {dueBlock.get('string')}")
            rrules_str = parse_date_from_text(dueBlock.get('string'))
            print(f'RRULES string: {rrules_str}')
            # What I want, is to pass dueBlock.get('String') to another function, which I'lld define earlier in the file


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

    if dueBlock: # if there is a date:
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