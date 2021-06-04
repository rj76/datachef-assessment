import collections
import datetime
import uuid


def round_to_quarter(minutes):
    base = 15
    return int(((base * (float(minutes)//base) + base) / 60) * 4)


def get_current_quarter():
    return round_to_quarter(datetime.datetime.now().minute)


def randomize_list(list_in):
    as_dict = {uuid.uuid4(): item for item in list_in}
    od = collections.OrderedDict(sorted(as_dict.items()))

    return list(od.values())


def qs_to_list(qs):
    return [item for item in qs]
