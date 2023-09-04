import time

import requests
from celery import shared_task
from django.db.models import Sum

from apps.main.admin import QR_code, Notifications, ReadNot
from apps.main.models import Token_confirm, Promo, Cashbek, PriceProduct, FINISH, Fribase
from apps.users.models import SimpleUsers
from config.settings import seller_bot, FIREBASE_KEY, FIREBASE_URL


@shared_task(bint=True)
def edit_qr_message(chat_id, message_id, pk):
    try:
        seller_bot.delete_message(chat_id=chat_id, message_id=message_id)
        seller_bot.send_message(chat_id=chat_id, text="Срок действия QR-кода истек")
        QR_code.objects.filter(pk=pk).delete()
    except:
        pass


@shared_task(bint=True)
def create_read(not_id):
    time.sleep(3)
    users = SimpleUsers.objects.all()
    notif = Notifications.objects.get(pk=int(not_id))
    read = []
    for i in users:
        read.append(ReadNot(user=i, notification=notif))
    ReadNot.objects.bulk_create(read)
    firebase = Fribase.objects.all()
    url = FIREBASE_URL
    header = {"Authorization": FIREBASE_KEY}
    body = {
        "to": "",
        "collapse_key": "type_a",
        "notification": {
            "title": notif.title_uz[:60],
            "body": notif.body_uz[:250]
        },
        "data": {
            "id": notif.id
        }
    }
    for i in firebase:
        body["to"] = i.fr_id
        requests.post(url=url, headers=header, json=body)

@shared_task(bint=True)
def edit_qr_done(chat_id, message_id, pk):
    try:
        seller_bot.delete_message(chat_id=chat_id, message_id=message_id)
        seller_bot.send_message(chat_id=chat_id, text="✅QR-код используется")
        QR_code.objects.filter(pk=pk).delete()
    except:
        pass


@shared_task(bint=True)
def delete_token(pk):
    try:
        Token_confirm.objects.filter(pk=pk).delete()
    except:
        pass


@shared_task(bint=True)
def check_promo(pk):
    promo = Promo.objects.get(pk=pk)
    incom = Cashbek.objects.filter(active=True, types=1, promo=promo)
    incom_sum = incom.aggregate(Sum('price'))['price__sum'] if incom.aggregate(Sum('price'))['price__sum'] else 0
    amount = promo.budget - incom_sum
    if PriceProduct.objects.filter(product=promo.products.filter(is_active=True).first(),
                                   promo=promo).first().all_price > amount:
        promo.status = FINISH
        promo.description = "Автоматически закрыто из-за исчерпания бюджета."
        promo.save()
