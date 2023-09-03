from django.db.models import Sum

from apps.main.models import Cashbek
from apps.users.models import *


def get_vendor_balance(user, vendor):
    user = SimpleUsers.objects.get(pk=user)
    alls = Cashbek.objects.filter(user=user, vendor_id=vendor, active=True)

    incom = alls.filter(user=user, types=1)
    expense = alls.filter(user=user, types=2)

    total_income = incom.aggregate(Sum('amount'))['amount__sum'] if incom.aggregate(Sum('amount'))['amount__sum'] else 0
    total_expense = expense.aggregate(Sum('amount'))['amount__sum'] if expense.aggregate(Sum('amount'))[
        'amount__sum'] else 0
    return total_income - total_expense
