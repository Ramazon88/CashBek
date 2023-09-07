from django.db import models
from django.db.models import Sum, F, Value
from django.db.models.functions import Concat

from apps.main.models import Cashbek
from apps.users.models import User
from config.settings import MEDIA_URL, DOMAIN

media_url = DOMAIN + MEDIA_URL


def get_balance(user):
    user = User.objects.get(phone=user).simple_user
    alls = Cashbek.objects.filter(user=user, active=True)
    incom = alls.filter(user=user, types=1)
    expense = alls.filter(user=user, types=2)
    queryset_incom = incom.annotate(
        vendor_logo=Concat(
            Value(media_url),
            F('vendor__logo'),
            output_field=models.CharField()
        )
    ).values('vendor__pk', 'vendor__name', 'vendor_logo').annotate(total=Sum('amount'))
    vendors = []
    for i in list(queryset_incom):
        total = 0
        obj = expense.filter(vendor__id=i["vendor__pk"]).aggregate(Sum('amount'))['amount__sum']
        if obj:
            total = obj
        vendors.append(
            {'id': i["vendor__pk"], 'name': i["vendor__name"], 'logo': i["vendor_logo"], 'total': i["total"] - total})

    return vendors


def get_all_balance(user, vendor=None):
    user = User.objects.get(phone=user).simple_user
    if vendor:
        alls = Cashbek.objects.filter(user=user, vendor_id=vendor, active=True)
    else:
        alls = Cashbek.objects.filter(user=user, active=True)
    incom = alls.filter(user=user, types=1)
    expense = alls.filter(user=user, types=2)
    total_income = incom.aggregate(Sum('amount'))['amount__sum'] if incom.aggregate(Sum('amount'))['amount__sum'] else 0
    total_expense = expense.aggregate(Sum('amount'))['amount__sum'] if expense.aggregate(Sum('amount'))[
        'amount__sum'] else 0
    data = {"total_income": total_income, "total_expense": total_expense}
    return data
