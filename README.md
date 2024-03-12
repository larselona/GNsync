
# Notion-GCal Sync

This Python script automates the synchronization of events between Google Calendar and Notion. It enables users to seamlessly update their Notion databases with events fetched from a specified Google Calendar, ensuring that important dates and tasks are accessible across both platforms.

## Description

The Notion-GCal Sync script provides a bridge between Google Calendar and Notion, allowing for the automatic transfer of event data into a Notion database. This project is particularly useful for users who rely on both Google Calendar for event scheduling and Notion for task and project management. By syncing events across platforms, this script ensures that all your information is up-to-date and centrally located.

Features include:
- Fetching events from Google Calendar.
- Creating and updating corresponding entries in a Notion database.
- Handling event deletions and modifications with ease.
- Using environment variables for configuration to keep sensitive information secure.

## Getting Started

### Dependencies

- Python 3.8+
- `google-auth`, `google-auth-oauthlib`, and `google-auth-httplib2` for Google API authentication.
- `google-api-python-client` for Google Calendar API.
- `notion-client` for interacting with Notion's API.
- `python-dotenv` for managing environment variables.

Ensure all dependencies are installed using the following command:
```sh
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client notion-client python-dotenv
```

### Installation

1. Clone the repository to your local machine.
   ```sh
   git clone https://github.com/your_username/Notion-GCal-Sync.git
   ```
2. Navigate into the cloned directory.
   ```sh
   cd Notion-GCal-Sync
   ```

### Configuration

1. Create a `.env` file in the root directory of the project.
2. Add the following lines, replacing the placeholders with your actual configuration values:
   ```
   SCOPES=https://www.googleapis.com/auth/calendar.readonly
   CREDENTIALS_FILE=path/to/your/credentials.json
   CALENDAR_ID=your_calendar_id@group.calendar.google.com
   NOTION_SECRET=your_notion_integration_secret
   DATABASE_ID=your_notion_database_id
   STUDENTS_DATABASE_ID=your_students_database_id
   ```

## Usage

To run the script and start the synchronization process, execute the following command in the root directory of the project:

```sh
python sync_script.py
```

This will fetch events from the specified Google Calendar and update the Notion database accordingly.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.


