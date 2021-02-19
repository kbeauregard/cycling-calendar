import datetime
import pickle
import os.path
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from cycling_calendar.scrape import get_description

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar",
]


class GoogleCalendar:
    _credentials = None

    def __init__(self):
        self.set_credentials()
        self.service = build("calendar", "v3", credentials=self._credentials)

    def set_credentials(self):
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                self._credentials = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self._credentials or not self._credentials.valid:
            if (
                self._credentials
                and self._credentials.expired
                and self._credentials.refresh_token
            ):
                self._credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                self._credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(self._credentials, token)

    def create_race_calendar(self):
        calendar = {"summary": "CyclingRaces", "timeZone": "America/Toronto"}

        return self.service.calendars().insert(body=calendar).execute()

    def create_event_from_race(self, calendar_id, race):
        description = ""

        if not pd.isna(race["WebSite"]):
            description = get_description(f'https://{race["WebSite"]}')
            if description:
                description = description + "\n"

            description = description + race["WebSite"]

        event = {
            "summary": f'{race["Name"]} ({race["Class"]})',
            "location": race["Country"].title(),
            "description": description,
            "start": {
                "dateTime": datetime.datetime.strptime(
                    race["Date From"], "%d/%m/%Y"
                ).isoformat(),
                "timeZone": "America/Toronto",
            },
            "end": {
                "dateTime": datetime.datetime.strptime(
                    race["Date To"], "%d/%m/%Y"
                ).isoformat(),
                "timeZone": "America/Toronto",
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "popup", "minutes": 10},
                ],
            },
        }

        self.service.events().insert(calendarId=calendar_id, body=event).execute()
