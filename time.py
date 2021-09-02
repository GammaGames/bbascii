from datetime import datetime, timedelta
import random


random.seed(datetime.now().strftime("%Y-%m-%d %H"))


def get_timestamp(date):
    return date.strftime("%Y-%m-%d %H:%M")


def get_season(date=None):
    """optional date must be provided in `%Y-%m-%d %H:%M` format"""
    if date is None:
        month = datetime.now().month
    else:
        month = datetime.strptime(date, "%Y-%m-%d %H:%M").month

    if 0 <= month <= 2:
        return "winter"
    elif 3 <= month <= 5:
        return "sprint"
    elif 6 <= month <= 8:
        return "summer"
    elif 9 <= month <= 11:
        return "fall"
    else:
        return "winter"


def get_time(date=None):
    """optional date must be provided in `%Y-%m-%d %H:%M` format"""
    if date is None:
        time = datetime.now().hour
    else:
        time = datetime.strptime(date, "%Y-%m-%d %H:%M").hour

    if 0 <= time <= 5:
        return "night"
    elif 6 <= time <= 11:
        return "morning"
    elif 12 <= time <= 16:
        return "afternoon"
    elif 17 <= time <= 19:
        return "evening"
    else:
        return "night"


def is_sunrise(date=None):
    """optional date must be provided in `%Y-%m-%d %H:%M` format"""
    if date is None:
        time = datetime.now().hour
    else:
        time = datetime.strptime(date, "%Y-%m-%d %H:%M").hour

    return time == 6


def is_sunset(date=None):
    """optional date must be provided in `%Y-%m-%d %H:%M` format"""
    if date is None:
        time = datetime.now().hour
    else:
        time = datetime.strptime(date, "%Y-%m-%d %H:%M").hour

    return time == 19


def get_weather(date=None):
    if date is None:
        time = datetime.now()
    else:
        time = datetime.strptime(date, "%Y-%m-%d %H:%M")

    state = random.getstate()
    random.seed(time.strftime("%Y-%m-%d %H"))
    val = random.random()
    special_val = random.random()
    random.setstate(state)

    season = get_season(get_timestamp(time))
    weather = "clear"
    special = None

    if val < 0.35:
        clouds = "clear"
    elif val < 0.5:
        clouds = "light"
    elif val < 0.75:
        clouds = "moderate"
    else:
        clouds = "dense"

    if season == "winter":
        if val < 0.45:
            weather = "clear"
        elif val < 0.8:
            weather = "snow"
        elif val < 0.95:
            weather = "snowstorm"
        else:
            weather = "blizzard"
    elif season == "spring":
        if val < 0.35:
            weather = "clear"
        elif val < 0.75:
            weather = "rain"
        else:
            weather = "rainstorm"

        if special_val > 0.95:
            special = "petals"
    elif season == "summer":
        if val < 0.5:
            weather = "clear"
        elif val < 0.95:
            weather = "rain"
        else:
            weather = "thunderstorm"
    elif season == "fall":
        if val < 0.5:
            weather = "clear"
        elif val < 0.95:
            weather = "rain"
        else:
            weather = "thunderstorm"

        if special_val > 0.95:
            special = "leaves"

    return clouds, weather, special


if __name__ == '__main__':
    print(get_season())
    print(get_season("2018-08-29 03:00"))
    print(get_time())
    print(get_time("2018-08-29 03:00"))
    print(is_sunrise())
    print(is_sunrise("2018-08-29 03:00"))
    print(is_sunset())
    print(is_sunset("2018-08-29 03:00"))
    print(get_weather())
    print(get_weather("2018-08-29 03:00"))

    print("---")
    date = datetime.now()
    for i in range(5):
        date += timedelta(hours=1)
        clouds, weather, special = get_weather(get_timestamp(date))
        print(f"{date.strftime('%Y-%m-%d %I:00')}: {clouds}, {weather}, {special}")

    print("---")
    date = datetime.now()
    for i in range(7):
        date += timedelta(days=1)
        date += timedelta(hours=1)
        clouds, weather, special = get_weather(get_timestamp(date))
        print(f"{date.strftime('%Y-%m-%d %I:00')}: {clouds}, {weather}, {special}")
