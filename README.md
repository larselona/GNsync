# Notion-GCal Sync

A refined Python utility for bidirectional synchronization between Google Calendar events and a Notion database. This tool is essential for those integrating their scheduling with project and task management across Google Calendar and Notion, ensuring cohesive and up-to-date management of dates, tasks, and events.

## Overview

This enhanced script facilitates a seamless integration between Google Calendar and Notion, automating the sync of events to maintain a centralized and current repository of your schedules and tasks.

Key features:
- Automated synchronization of events from Google Calendar to Notion.
- Efficient handling of event updates and deletions.
- Configuration via a separate file to secure sensitive information.

## Setup

### Prerequisites

- Python 3.8 or later.
- Libraries: `google-auth`, `google-api-python-client`, `notion-client`.
- A configuration file for sensitive information.

Install dependencies with:
```sh
pip install google-auth google-api-python-client notion-client
```

### Getting Started

1. Clone the repository:
   ```sh
   git clone https://github.com/your_username/Notion-GCal-Sync.git
   ```
2. Enter the project directory:
   ```sh
   cd Notion-GCal-Sync
   ```

### Configuration

1. Ensure a `config.py` file exists in the project root with your settings:
   ```python
   SCOPES=['https://www.googleapis.com/auth/calendar.readonly']
   SERVICE_ACCOUNT_FILE='path/to/your/service-account-file.json'
   NOTION_TOKEN="your-secret-notion-token"
   DATABASE_ID="your-notion-database-id"
   STUDENTS_DATABASE_ID='your-students-database-id'
   CALENDAR_ID='your-calendar-id@group.calendar.google.com'
   ```

## Execution

Run the script from the project's root to start syncing:
```sh
python sync_script.py
```

## Engagement

Contributions to the project are welcome. Enhance the tool by:
1. Forking the project.
2. Creating a branch for your feature (`git checkout -b feature/YourFeature`).
3. Committing your changes (`git commit -m 'Introduce YourFeature'`).
4. Pushing to the branch (`git push origin feature/YourFeature`).
5. Opening a pull request.

## License

Distributed under the MIT License. See `LICENSE` for more information.