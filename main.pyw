from datetime import date
import json
import time
import subprocess

allowed_hours_in_weekends = 4
allowed_hours_in_week_days = 1

while True:
    _today = date.today()
    today = _today.strftime("%d/%m/%Y")

    day_name = _today.strftime("%A")

    if day_name in ("Saturday", "Sunday"):
        allowed_seconds = allowed_hours_in_weekends * 60 * 60
    else:
        allowed_seconds = allowed_hours_in_week_days * 60 * 60

    try:
        with open('log', "r") as log_file:
            data = json.load(log_file)

        if data["today"] != today:
            data["today"] = today
            data["played_seconds"] = 0

    except (FileNotFoundError, json.JSONDecodeError):
        data = {
            "today": today,
            "played_seconds": 0
        }

    print(f'Allowed seconds: {allowed_seconds}')
    print(f'Current played seconds: {data["played_seconds"]}')

    if data["played_seconds"] < allowed_seconds:
        data["played_seconds"] += 5
        print("Added 5 seconds.")

    else:
        print("Exceeded the time limit. Shutting down...")
        subprocess.Popen("shutdown -s")
        # subprocess.Popen("dxdiag")
        exit()

    with open('log', "w+") as log_file:
        json.dump(data, log_file)
        print("Dumped.\n")

    time.sleep(5)
