import datetime as dt
import requests


def fetch_schedule(auth: str) -> list[dict] | None:
    DATE_FMT = "%Y-%m-%d"

    date_start = dt.datetime.now()
    date_end = date_start + dt.timedelta(days=32)

    date_start_fmt = date_start.strftime(DATE_FMT)
    date_end_fmt = date_end.strftime(DATE_FMT)

    resp = requests.get("https://my.itmo.ru/api/schedule/schedule/personal",
                        headers={"Content-Type": "application/json",
                                 "Authorization": auth.encode()},
                        params={"date_start": date_start_fmt,
                                "date_end": date_end_fmt})
    json = resp.json()

    if "data" in json:
        return json["data"]
    return None


def parse_schedule(schedule: list[dict]) -> list[dict]:
    DATE_RAW_FMT = "%Y-%m-%d"
    TIME_RAW_FMT = "%H:%M"

    result = []

    for day in schedule:
        date = day["date"]
        date_fmt = dt.datetime.strptime(date, DATE_RAW_FMT)

        for lesson in day["lessons"]:
            start_time = lesson["time_start"]
            end_time = lesson["time_end"]

            start_time_fmt = dt.datetime.strptime(start_time, TIME_RAW_FMT)
            end_time_fmt = dt.datetime.strptime(end_time, TIME_RAW_FMT)

            start_datetime = dt.datetime.combine(date_fmt.date(),
                                                 start_time_fmt.time())
            end_datetime = dt.datetime.combine(date_fmt.date(),
                                               end_time_fmt.time())

            shift = dt.timedelta(hours=3)
            start_datetime -= shift
            end_datetime -= shift

            start_datetime = start_datetime.strftime("%Y%m%dT%H%M%SZ")
            end_datetime = end_datetime.strftime("%Y%m%dT%H%M%SZ")

            event = {}
            event["Subject"] = lesson["subject"]
            event["Datetime start"] = start_datetime
            event["Datetime end"] = end_datetime
            event["Description"] = (
                f"{lesson['type']}"
                "\\n"
                f"{lesson['teacher_name']}"
                "\\n"
                f"{lesson['format']}"
                "\\n"
                f"{lesson['building']}"
            )
            result.append(event)

    return result


def cnvt_schedule_to_ics(schedule: list[dict]) -> str:
    result = ""

    result += "BEGIN:VCALENDAR\n"
    result += "VERSION:2.0\n"
    result += "PRODID:-//Apple Computer\\, Inc//iCal 1.5//EN\n"
    result += "CALSCALE:GREGORIAN\n"
    result += "X-WR-CALNAME:my.itmo\n"
    result += "X-WR-TIMEZONE:Etc/UTC\n"
    result += "X-PUBLISHED-TTL:PT10M\n"
    result += "REFRESH-INTERVAL;VALUE=DURATION:PT10M\n"
    for event in schedule:
        result += "BEGIN:VEVENT\n"
        result += f"SUMMARY:{event['Subject']}\n"
        result += f"DTSTART;VALUE=DATE-TIME:{event['Datetime start']}\n"
        result += f"DTEND;VALUE=DATE-TIME:{event['Datetime end']}\n"
        result += f"DESCRIPTION:{event['Description']}\n"
        result += "END:VEVENT\n"
    result += "END:VCALENDAR"

    return result
