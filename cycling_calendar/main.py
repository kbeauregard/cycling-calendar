import pandas as pd
from tqdm import tqdm

from cycling_calendar.google_calendar import GoogleCalendar

RACE_CLASSES_TO_ADD = ["2.UWT", "1.UWT", "2.1"]


def read_race_data():
    racing_data = pd.read_excel("cyclingcalendar/race_calendar.xlsx")
    # Fix the column names being set as the first row instead
    racing_data.columns = racing_data.iloc[0]
    racing_data = racing_data.drop([0])
    racing_data = racing_data[racing_data["Class"].isin(RACE_CLASSES_TO_ADD)]

    return racing_data


def main():
    calendar_api = GoogleCalendar()
    racing_calendar = calendar_api.create_race_calendar()

    racing_data = read_race_data()

    for index, race in tqdm(racing_data.iterrows()):
        calendar_api.create_event_from_race(racing_calendar["id"], race)


if __name__ == "__main__":
    main()
