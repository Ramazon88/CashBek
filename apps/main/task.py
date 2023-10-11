import datetime

import requests
from celery import shared_task
from django.contrib.auth.models import Group
from django.db.models import Sum, Q

from apps.main.admin import QR_code, Notifications, ReadNot
from apps.main.models import Token_confirm, Promo, Cashbek, PriceProduct, FINISH, Fribase, WAIT, ACTIVE, PAUSE
from apps.users.models import SimpleUsers, User
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


@shared_task(bint=True)
def cashbek_message(pk):
    obj = Cashbek.objects.get(pk=pk)
    if obj.types == 1:
        text = f"<strong>🟢Клиент получил кэшбэк</strong>\n\n<strong>Модел: </strong>{obj.product.model}\n"
        text += f"<strong>IMEI: </strong><code>{obj.product.imei1}</code>\n"
        text += f"<strong>SKU: </strong>{obj.product.sku}\n"
        text += "<strong>Сумма кэшбэка: </strong>" + "{:,}\n".format(obj.amount)
        text += f"<strong>Клиент: </strong>{obj.user.first_name}\n"
    else:
        text = f"<strong>🔴Клиент использовал кэшбэк. Ваш счет пополнен</strong>\n\n<strong>Модел: </strong>{obj.product.model}\n"
        text += f"<strong>IMEI: </strong><code>{obj.product.imei1}</code>\n"
        text += f"<strong>SKU: </strong>{obj.product.sku}\n"
        text += "<strong>Использованная сумма: </strong>" + "{:,}\n".format(obj.amount)
        text += f"<strong>Клиент: </strong>{obj.user.first_name}\n"
    seller_bot.send_message(chat_id=obj.seller.telegram_id, text=text, parse_mode="HTML")


@shared_task(bint=True)
def set_manager_group(phone):
    User.objects.get(phone=phone).groups.add(Group.objects.get(name="Manager"))


@shared_task(bint=True)
def check_many_cashbek(user_pk):
    date = datetime.date.today()
    user = SimpleUsers.objects.get(pk=user_pk)
    cashbek = Cashbek.objects.filter(types=1, active=True, created_at__date=date, user__pk=user_pk)
    if cashbek.count() > 2:
        text = f"<strong>🔴Клиент получил более 2 кэшбэков</strong>\n\n<strong>Количество полученных кэшбэков: </strong>{cashbek.count()}\n"
        text += f"<strong>Клиент: </strong>{user.first_name} {user.last_name}\n"
        text += f"<strong>Номер телефона: </strong><code>{user.simple_user.phone}</code>\n"
        seller_bot.send_message(chat_id=-4058643019, text=text, parse_mode="HTML")


@shared_task(bint=True)
def check_promo_expire():
    date = datetime.date.today()
    promo = Promo.objects.filter(Q(status=WAIT) | Q(status=ACTIVE) | Q(status=PAUSE), end=date)
    for i in promo:
        i.status = FINISH
        i.description = "Акция была автоматически отменена в связи с истечением срока действия"
        i.save()

