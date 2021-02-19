# Google Calendar Racing Schedule
[![Generic badge](https://img.shields.io/badge/season-2021-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/psf/black)

Adds 2.UWT, 1.UWT and 2.1 cycling races for the year to your Google calendar

## Setup

### Credentials

Creates your Google app and authorizes it

1. Visit Google Quickstart [here](https://developers.google.com/calendar/quickstart/python)
2. Click `Enable the Google Calendar API` button and follow the instructions
3. Place the `credentials.json` file in the root of this project
4. Later during first run you will need to sign in through the browser to authorize the application to add a new calendar as well as add events
###### Note: Google will warn you about the application not being verified, you can ignore this since you are the application owner

### Quick Start

```bash
pip install -r requirements.txt
PYTHONPATH=. python cycling_calendar/main.py
```

## Updating the data

1. Visit the UCI road race calendar [here](https://www.uci.org/road/calendar)
2. Click `Export more data` and save to excel
3. Rename the downloaded excel to `race_calendar.xlsx`
4. Replace `cycling_calendar/race_calendar.xlsx` with your new excel sheet
