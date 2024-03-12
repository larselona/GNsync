import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from notion_client import Client

# Load environment variables
load_dotenv()

# Setup Google Calendar API
SCOPES = [os.getenv('SCOPES')]
CREDENTIALS_FILE = os.getenv('CREDENTIALS_FILE')
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
else:
    creds = None

# Check if we have valid credentials, if not, log in or refresh
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('calendar', 'v3', credentials=creds)

# Fetch events from Google Calendar
calendar_id = os.getenv('CALENDAR_ID')
events_result = service.events().list(calendarId=calendar_id, timeMin=(datetime.utcnow() - timedelta(weeks=1)).isoformat() + 'Z', maxResults=300, singleEvents=True, orderBy='startTime').execute()
events = events_result.get('items', [])
current_google_event_ids = set(event['id'] for event in events)

# Setup Notion Client
notion = Client(auth=os.getenv('NOTION_SECRET'))
database_id = os.getenv('DATABASE_ID')

# Determine one week ago as an offset-aware datetime for comparison
one_week_ago = datetime.utcnow().replace(tzinfo=timezone.utc) - timedelta(weeks=1)

# Fetch all student entries and event IDs from Notion
students_database_id = os.getenv('STUDENTS_DATABASE_ID')
students_response = notion.databases.query(database_id=students_database_id)
students = students_response.get("results", [])

student_name_to_id = {student["properties"]["Name"]["title"][0]["text"]["content"]: {"id": student["id"], "euro": student["properties"]["€"]["number"] if "€" in student["properties"] else 0} for student in students}

notion_synced_events_query = notion.databases.query(
    database_id=database_id,
    filter={"property": "Event ID", "rich_text": {"is_not_empty": True}},
)
notion_synced_event_ids = set(page["properties"]["Event ID"]["rich_text"][0]["text"]["content"] for page in notion_synced_events_query.get("results", []))

# Process each Google Calendar event (creation/update logic should be here)
for event in events:
    event_name = event.get('summary', 'No Title')
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))
    google_event_id = event['id']
    
    student_info = student_name_to_id.get(event_name)
    student_relation = []
    euro_value = 0  # Default value if no match is found
    
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
            database_id=database_id,
            filter={"property": "Event ID", "rich_text": {"equals": google_event_id}},
        )
        if query_result['results']:
            page_id = query_result['results'][0]['id']
            notion.pages.update(page_id=page_id, properties=properties)
        else:
            notion.pages.create(parent={"database_id": database_id}, properties=properties)
    except Exception as e:
        print(f"Error processing event '{event_name}': {e}")

# Handle genuinely deleted events
deleted_event_ids = notion_synced_event_ids - current_google_event_ids

for deleted_event_id in deleted_event_ids:
    page_to_delete_query = notion.databases.query(
        database_id=database_id,
        filter={"property": "Event ID", "rich_text": {"equals": deleted_event_id}},
    )
    if page_to_delete_query["results"]:
        for page in page_to_delete_query["results"]:
            page_to_delete_id = page['id']
            try:
                notion.pages.update(
                    page_id=page_to_delete_id,
                    properties={"Deleted": {"checkbox": True}}
                )
                print(f"Marked event {deleted_event_id} as deleted in Notion.")
            except Exception as e:
                print(f"Failed to mark event {deleted_event_id} as deleted: {e}")

print("Sync and cleanup complete.")
