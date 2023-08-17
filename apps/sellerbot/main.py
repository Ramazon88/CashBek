import datetime

from telegram import Update
from telegram.ext import CallbackContext

from apps.main.models import Products, ACTIVE, PriceProduct
from apps.sellerbot.buttons import *
from apps.sellerbot.models import SellerTemp
from apps.users.models import Seller


def start_handler(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)
    try:
        seller = Seller.objects.get(telegram_id=user_id, seller__is_active=True)
        text = f"<strong>Продавец: </strong>{seller.name}\n<strong>ID: </strong><code>{seller.telegram_id}</code>"
        update.message.reply_html(text, reply_markup=main_buttons)
        try:
            obj = SellerTemp.objects.get(tg_id=user_id)
            obj.step = 0
            obj.save()
        except:
            SellerTemp.objects.create(tg_id=user_id, step=0)
    except Exception as e:
        print(e)


def core(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)
    try:
        seller = Seller.objects.get(telegram_id=user_id, seller__is_active=True)
        msg = update.message.text
        step = SellerTemp.objects.get(tg_id=user_id)
        if step.step == 0 and msg == 'Начисление Кэшбэка':
            SellerTemp.objects.filter(tg_id=user_id).update(step=1, qr_type=1)
            update.message.reply_html("Введите IMEI или серийный номер", reply_markup=home_button)
        elif step.step == 1 and msg != '🏠Главный страница':
            SellerTemp.objects.filter(tg_id=user_id).update(step=2, imei=msg)
            if step.qr_type == 1:
                objs = Products.objects.filter(imei1=msg, is_active=True)
                if objs.exists():
                    today = datetime.datetime.today()
                    promo = objs.first().promo.filter(start__lte=today, end__gte=today, status=ACTIVE)
                    if promo.exists():
                        SellerTemp.objects.filter(tg_id=user_id).update(step=2, imei=msg)
                        update.message.reply_html(f"<strong>Модел: </strong>{objs.first().model}\n"
                                                  f"<strong>IMEI: </strong><code>{objs.first().imei1}</code>\n"
                                                  f"<strong>SKU: </strong>{objs.first().sku}\n"
                                                  "<strong>Сумма кэшбэка: </strong>" + "{:,}".format(PriceProduct.objects.get(product=objs.first(),
                                                                                                                                  promo=promo.first()).price) + " Cум\n\n"
                                                  "Продукт и акция активны в данный момент. Нажмите на кнопку ниже, чтобы воспользоваться акцией👇",
                                                  reply_markup=qr_button)
                    else:
                        SellerTemp.objects.filter(tg_id=user_id).update(step=0)
                        update.message.reply_html(f"<strong>Модел: </strong>{objs.first().model}\n<strong>IMEI: "
                                                  f"</strong><code>{objs.first().imei1}</code>\n\n"
                                                  "<i>❌Этот товар недоступен ни в одной акции</i>",
                                                  reply_markup=main_buttons)
                else:
                    SellerTemp.objects.filter(tg_id=user_id).update(step=0)
                    update.message.reply_html("❌Нет активного продукта с таким IMEI или серийным номером", reply_markup=main_buttons)
        elif msg == '🏠Главный страница':
            SellerTemp.objects.filter(tg_id=user_id).update(step=0)
            update.message.reply_html("Главный страница", reply_markup=main_buttons)
    except Exception as e:
        print(e)