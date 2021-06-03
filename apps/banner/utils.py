import datetime


def round_to_quarter(minutes):
    base = 15
    return int(((base * (float(minutes)//base) + base) / 60) * 4)


def get_current_quarter():
    return round_to_quarter(datetime.datetime.now().minute)
