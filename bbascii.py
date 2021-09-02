from sh import calendar, fortune
from datetime import datetime
import random
import click
import random


# print(calendar())
# print(fortune("-s", "/usr/share/games/fortunes/literature"))


@click.command()
@click.argument("date", type=click.DateTime(), required=False)
def main(date):
    if date is None:
        date = datetime.now()

    random.seed(date.strftime("%Y-%m-%d %H"))

    calendar_day = date.strftime("%m%d")
    birthdays = calendar(
        "-l", 10,
        "-t", calendar_day,
        "-f", "/usr/share/calendar/calendar.birthday"
    ).split("\n")
    random.shuffle(birthdays)
    birthdays = list(filter(len, birthdays))[:2]
    print("Birthdays:")
    for birthday in birthdays:
        print(birthday)

    us_holidays = calendar(
        "-l", 10,
        "-t", calendar_day,
        "-f", "/usr/share/calendar/calendar.usholiday"
    ).split("\n")
    random.shuffle(us_holidays)
    us_holidays = list(filter(len, us_holidays))[:2]
    print("Holidays:")
    for us_holiday in us_holidays:
        print(us_holiday)

    holidays = calendar(
        "-l", 10,
        "-t", calendar_day,
        "-f", f"/usr/share/calendar/calendar.{random.choice(['computer', 'holiday', 'lotr', 'world'])}"
    ).split("\n")
    if len(holidays) == 0:
        holidays = calendar(
            "-l", 10,
            "-t", calendar_day,
            "-f", f"/usr/share/calendar/calendar.{random.choice(['holiday', 'lotr', 'world'])}"
        ).split("\n")

    random.shuffle(holidays)
    holidays = list(filter(len, holidays))[:3]
    for holiday in holidays:
        print(holiday)

    print("Fortune:")
    fortunes = fortune("-s").rstrip("\n")
    print(fortunes)


    # print(calendar_day)


if __name__ == "__main__":
    main()
