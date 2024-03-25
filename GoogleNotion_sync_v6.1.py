import os
from datetime import datetime, timedelta, timezone
from google.oauth2 import service_account
from googleapiclient.discovery import build
from notion_client import Client
import logging
from config import SCOPES, SERVICE_ACCOUNT_FILE, NOTION_TOKEN, DATABASE_ID, STUDENTS_DATABASE_ID, CALENDAR_ID

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Authenticate using the service account for Google Calendar API
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=creds)

# Fetch events from Google Calendar
events_result = service.events().list(
    calendarId=CALENDAR_ID,
    timeMin=(datetime.utcnow() - timedelta(weeks=1)).isoformat() + 'Z',
    maxResults=200,
    singleEvents=True,
    orderBy='startTime',
).execute()
events = events_result.get('items', [])

# Setup Notion Client
notion = Client(auth=NOTION_TOKEN)

# Fetch all student entries and event IDs from Notion
students_response = notion.databases.query(database_id=STUDENTS_DATABASE_ID)
students = students_response.get("results", [])

student_name_to_id = {student["properties"]["Name"]["title"][0]["text"]["content"]: {"id": student["id"], "euro": student["properties"]["€"]["number"] if "€" in student["properties"] else 0} for student in students}

notion_synced_events_query = notion.databases.query(
    database_id=DATABASE_ID,
    filter={"property": "Event ID", "rich_text": {"is_not_empty": True}},
)
notion_synced_event_ids = {page["properties"]["Event ID"]["rich_text"][0]["text"]["content"] for page in notion_synced_events_query.get("results", [])}

for event in events:
    event_name = event.get('summary', 'No Title')
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))
    google_event_id = event['id']
    
    student_info = student_name_to_id.get(event_name, None)
    student_relation = []
    euro_value = 0
    
    if student_info:
        student_relation = [{"id": student_info["id"]}]
        euro_value = student_info["euro"]
    
    properties = {
        "Name": {"title": [{"text": {"content": event_name}}]},
        "Student": {"relation": student_relation},
        "€": {"number": euro_value},
        "Event ID": {"rich_text": [{"text": {"content": google_event_id}}]},
        "Last Sync": {"date": {"start": datetime.utcnow().isoformat() + 'Z'}}
    }
    
    if start and end:
        properties["Start"] = {"date": {"start": start, "end": end}}
    
    try:
        query_result = notion.databases.query(
            database_id=DATABASE_ID,
            filter={"property": "Event ID", "rich_text": {"equals": google_event_id}},
        )
        if query_result['results']:
            page_id = query_result['results'][0]['id']
            notion.pages.update(page_id=page_id, properties=properties)
        else:
            notion.pages.create(parent={"database_id": DATABASE_ID}, properties=properties)
    except Exception as e:
        logging.error(f"Error processing event '{event_name}': {e}")

print("Sync and cleanup complete.")
