import json
import os
import subprocess
import time
from datetime import date

allowed_hours_in_weekends = 10
allowed_hours_in_week_days = 8

show_remaining_time_in_desktop = True
log_file_path = "log"
check_interval = 5


class DifferentDay(Exception):
    pass


def parse_seconds_to_str(total_seconds: float = 0) -> str:
    """This is a function I wrote in a different project."""

    def plural_check(n: float):
        return 's' if n > 1 else ''

    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    months, weeks = divmod(weeks, 4)

    str_blocks = list()
    # this may be optimized but idk
    if months > 0:
        str_blocks.append(f'{months} month{plural_check(months)}')
    if weeks > 0:
        str_blocks.append(f'{weeks} week{plural_check(weeks)}')
    if days > 0:
        str_blocks.append(f'{days} day{plural_check(days)}')
    if hours > 0:
        str_blocks.append(f'{hours} hour{plural_check(hours)}')
    if minutes > 0:
        str_blocks.append(f'{minutes} minute{plural_check(minutes)}')
    if seconds > 0:
        str_blocks.append(f'{seconds} second{plural_check(seconds)}')

    return " ".join(str_blocks)


def update_remaining_time_file(remaining: int):
    with open(os.environ['USERPROFILE'] + "\Desktop\Time Remaining.txt", "w+") as file:
        file.write("Time remaining: " + parse_seconds_to_str(remaining))


if __name__ == '__main__':
    while True:
        _today = date.today()

        today_date = _today.strftime("%d/%m/%Y")
        day_name = _today.strftime("%A")

        # weekend check
        if day_name in ("Saturday", "Sunday"):
            allowed_seconds = allowed_hours_in_weekends * 60 * 60
        else:
            allowed_seconds = allowed_hours_in_week_days * 60 * 60

        # read the log
        try:
            with open(log_file_path, "r") as log_file:
                log = json.load(log_file)
                if log["date"] != today_date:
                    raise DifferentDay  # reset

        except (FileNotFoundError, DifferentDay, KeyError, json.JSONDecodeError):
            log = {"date"          : today_date,
                   "session_length": 0}

        print(f'Allowed time length\t: {parse_seconds_to_str(allowed_seconds)}')
        print(f'Current session length\t: {parse_seconds_to_str(log["session_length"])}')

        if log["session_length"] < allowed_seconds:
            log["session_length"] += check_interval

        else:
            print("Exceeded the time limit. Shutting down...")
            subprocess.Popen("shutdown -s")
            exit()

        with open('log', "w+") as log_file:
            json.dump(log, log_file)

        print(f"Added {check_interval} seconds and dumped to the log file.")
        if show_remaining_time_in_desktop:
            update_remaining_time_file(allowed_seconds - log["session_length"])
            print("Updated the remaining time file on Desktop.")

        print()
        time.sleep(check_interval)
