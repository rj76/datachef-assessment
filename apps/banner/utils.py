import collections
import datetime
import uuid

from django.db.models import Sum, Subquery, OuterRef

from apps.banner import models


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


def aggregate_revenue():
    models.Click.objects.filter(conversions__revenue__gt=0).update(
        conversion_revenue_sum=Subquery(
            models.Click.objects.filter(
                click_id=OuterRef('click_id')
            ).annotate(
                total=Sum('conversions')
            ).values('total')[:1]
        )
    )
