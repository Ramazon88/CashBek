import datetime

from django.utils import timezone
from telegram import Update, InputFile
from telegram.ext import CallbackContext
import qrcode
from io import BytesIO
from apps.main.models import Products, ACTIVE, PriceProduct, QR_code, INCOME, Token_confirm, EXPENSE
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
        elif step.step == 0 and msg == 'Cписание Кэшбэка':
            SellerTemp.objects.filter(tg_id=user_id).update(step=1, qr_type=2)
            update.message.reply_html("Введите IMEI или серийный номер", reply_markup=home_button)
        elif step.step == 1 and msg != '🏠Главный страница':
            SellerTemp.objects.filter(tg_id=user_id).update(step=2, imei=msg)
            if step.qr_type == 1:
                objs = Products.objects.filter(imei1=msg, is_active=True)
                if objs.exists():
                    today = timezone.now()
                    promo = objs.first().promo.filter(start__lte=today, end__gte=today, status=ACTIVE)
                    if promo.exists():
                        qr_obj = QR_code.objects.filter(product=objs.first(), is_used=False, expiry_date__gt=today)
                        if qr_obj.exists():
                            SellerTemp.objects.filter(tg_id=user_id).update(step=0)
                            update.message.reply_html(f"<strong>Модел: </strong>{objs.first().model}\n<strong>IMEI: "
                                                      f"</strong><code>{objs.first().imei1}</code>\n\n"
                                                      "<i>❌Есть активный QR-код</i>",
                                                      reply_markup=main_buttons)
                        else:
                            SellerTemp.objects.filter(tg_id=user_id).update(step=2, imei=msg)
                            update.message.reply_html(f"<strong>Модел: </strong>{objs.first().model}\n"
                                                      f"<strong>IMEI: </strong><code>{objs.first().imei1}</code>\n"
                                                      f"<strong>SKU: </strong>{objs.first().sku}\n"
                                                      "<strong>Сумма кэшбэка: </strong>" + "{:,}".format(
                                PriceProduct.objects.get(product=objs.first(),
                                                         promo=promo.first()).price) + " Cум\n"
                                                                                       f"<strong>Тип: </strong>Начисление Кэшбэка\n\n"
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
                    update.message.reply_html("❌Нет активного продукта с таким IMEI или серийным номером",
                                              reply_markup=main_buttons)

            elif step.qr_type == 2:
                objs = Products.objects.filter(imei1=msg, is_active=True)
                if objs.exists():
                    today = timezone.now()
                    promo = objs.first().promo.filter(start__lte=today, end__gte=today, status=ACTIVE)
                    qr_obj = QR_code.objects.filter(product=objs.first(), is_used=False, expiry_date__gt=today)
                    if qr_obj.exists():
                        SellerTemp.objects.filter(tg_id=user_id).update(step=0)
                        update.message.reply_html(f"<strong>Модел: </strong>{objs.first().model}\n<strong>IMEI: "
                                                  f"</strong><code>{objs.first().imei1}</code>\n\n"
                                                  "<i>❌Есть активный QR-код</i>",
                                                  reply_markup=main_buttons)
                    else:
                        SellerTemp.objects.filter(tg_id=user_id).update(step=2, imei=msg)
                        update.message.reply_html(f"<strong>Модел: </strong>{objs.first().model}\n"
                                                  f"<strong>IMEI: </strong><code>{objs.first().imei1}</code>\n"
                                                  f"<strong>SKU: </strong>{objs.first().sku}\n"
                                                  "<strong>Сумма кэшбэка: </strong>" + "{:,}".format(
                            PriceProduct.objects.get(product=objs.first(),
                                                     promo=promo.first()).price if promo.exists() else 0) + " Cум\n"
                                                                                   f"<strong>Тип: </strong>Cписание Кэшбэка\n\n"
                                                                                   "Продукт активны в данный момент. Нажмите кнопку ниже, чтобы получить кэшбэк👇",
                                                  reply_markup=qr_button)
                else:
                    SellerTemp.objects.filter(tg_id=user_id).update(step=0)
                    update.message.reply_html("❌Нет активного продукта с таким IMEI или серийным номером",
                                              reply_markup=main_buttons)

        elif step.step == 2 and msg == 'Генерация QR-кода':
            if step.qr_type == 1:
                objs = Products.objects.filter(imei1=step.imei, is_active=True)
                if objs.exists():
                    today = timezone.now()
                    promo = objs.first().promo.filter(start__lte=today, end__gte=today, status=ACTIVE)
                    if promo.exists():
                        qr_obj = QR_code.objects.filter(product=objs.first(), is_used=False, expiry_date__gt=today)
                        if qr_obj.exists():
                            SellerTemp.objects.filter(tg_id=user_id).update(step=0, imei=msg)
                            update.message.reply_html(f"<strong>Модел: </strong>{objs.first().model}\n<strong>IMEI: "
                                                      f"</strong><code>{objs.first().imei1}</code>\n\n"
                                                      "<i>❌Есть активный QR-код</i>",
                                                      reply_markup=main_buttons)
                        else:
                            if Token_confirm.objects.filter(product=objs.first(), expiry_date__gt=today).exists():
                                SellerTemp.objects.filter(tg_id=user_id).update(step=0, imei=msg)
                                update.message.reply_html(
                                    f"<strong>Модел: </strong>{objs.first().model}\n<strong>IMEI: "
                                    f"</strong><code>{objs.first().imei1}</code>\n\n"
                                    "<i>❌Товар находится в процессе покупки в другом сеансе</i>",
                                    reply_markup=main_buttons)
                            else:
                                qr_code = QR_code.objects.create(product=objs.first(), types=INCOME, seller=Seller.objects.get(telegram_id=user_id))
                                qr = qrcode.QRCode(
                                    version=1,
                                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                                    box_size=10,
                                    border=4,
                                )
                                qr.add_data(qr_code.qr_id)
                                qr.make(fit=True)
                                img_stream = BytesIO()
                                qr.make_image(fill_color="green", back_color="white").save(img_stream)
                                binary_data = img_stream.getvalue()
                                message = update.message.reply_photo(photo=InputFile(binary_data),
                                                                     caption="Тип <strong>Начисление Кэшбэка</strong>\n"
                                                                             "Срок действия <strong>2 минуты</strong>\n"
                                                                             f"{qr_code.qr_id}",
                                                                     parse_mode="HTML")
                                qr_code.message_id = message["message_id"]
                                qr_code.chat_id = user_id
                                qr_code.save_edit()
                                SellerTemp.objects.filter(tg_id=user_id).update(step=0)
                                update.message.reply_html("Главный страница", reply_markup=main_buttons)

                    else:
                        SellerTemp.objects.filter(tg_id=user_id).update(step=0)
                        update.message.reply_html(f"<strong>Модел: </strong>{objs.first().model}\n<strong>IMEI: "
                                                  f"</strong><code>{objs.first().imei1}</code>\n\n"
                                                  "<i>❌Этот товар недоступен ни в одной акции</i>",
                                                  reply_markup=main_buttons)
                else:
                    SellerTemp.objects.filter(tg_id=user_id).update(step=0)
                    update.message.reply_html("❌Нет активного продукта с таким IMEI или серийным номером",
                                              reply_markup=main_buttons)
            elif step.qr_type == 2:
                objs = Products.objects.filter(imei1=step.imei, is_active=True)
                if objs.exists():
                    today = timezone.now()
                    qr_obj = QR_code.objects.filter(product=objs.first(), is_used=False, expiry_date__gt=today)
                    if qr_obj.exists():
                        SellerTemp.objects.filter(tg_id=user_id).update(step=0, imei=msg)
                        update.message.reply_html(f"<strong>Модел: </strong>{objs.first().model}\n<strong>IMEI: "
                                                  f"</strong><code>{objs.first().imei1}</code>\n\n"
                                                  "<i>❌Есть активный QR-код</i>",
                                                  reply_markup=main_buttons)
                    else:
                        if Token_confirm.objects.filter(product=objs.first(), expiry_date__gt=today).exists():
                            SellerTemp.objects.filter(tg_id=user_id).update(step=0, imei=msg)
                            update.message.reply_html(
                                f"<strong>Модел: </strong>{objs.first().model}\n<strong>IMEI: "
                                f"</strong><code>{objs.first().imei1}</code>\n\n"
                                "<i>❌Товар находится в процессе покупки в другом сеансе</i>",
                                reply_markup=main_buttons)
                        else:
                            qr_code = QR_code.objects.create(product=objs.first(), types=EXPENSE, seller=Seller.objects.get(telegram_id=user_id))
                            qr = qrcode.QRCode(
                                version=1,
                                error_correction=qrcode.constants.ERROR_CORRECT_L,
                                box_size=10,
                                border=4,
                            )
                            qr.add_data(qr_code.qr_id)
                            qr.make(fit=True)
                            img_stream = BytesIO()
                            qr.make_image(fill_color="red", back_color="white").save(img_stream)
                            binary_data = img_stream.getvalue()
                            message = update.message.reply_photo(photo=InputFile(binary_data),
                                                                 caption="Тип <strong>Cписание Кэшбэка</strong>\n"
                                                                 "Срок действия <strong>2 минуты</strong>\n"
                                                                 f"{qr_code.qr_id}",
                                                                 parse_mode="HTML")
                            qr_code.message_id = message["message_id"]
                            qr_code.chat_id = user_id
                            qr_code.save_edit()
                            SellerTemp.objects.filter(tg_id=user_id).update(step=0)
                            update.message.reply_html("Главный страница", reply_markup=main_buttons)


                else:
                    SellerTemp.objects.filter(tg_id=user_id).update(step=0)
                    update.message.reply_html("❌Нет активного продукта с таким IMEI или серийным номером",
                                              reply_markup=main_buttons)



        elif msg == '🏠Главный страница':
            SellerTemp.objects.filter(tg_id=user_id).update(step=0)
            update.message.reply_html("Главный страница", reply_markup=main_buttons)
    except Exception as e:
        print(e)
