import datetime as dt
import requests


def fetch_schedule(auth: str) -> list[dict] | None:
    DATE_FMT = "%Y-%m-%d"

    date_start = dt.datetime.now()
    date_end = date_start + dt.timedelta(days=3)

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


def parse_schedule(schedule: list[dict]) -> dict:
    result = {}

    for day in schedule:
        date = day["date"]
        pairs = day["lessons"]

        print(date)
        for pair in pairs:
            p_name = pair["subject"]
            p_type = pair["type"]
            p_ts = pair["time_start"]
            p_te = pair["time_end"]
            p_teacher = pair["teacher_name"]

            print(p_name, p_type, p_ts, p_te, p_teacher)

    return result
