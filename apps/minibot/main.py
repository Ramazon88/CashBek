from telegram import Update, InputMediaPhoto
from telegram.ext import CallbackContext

from apps.minibot.buttons import main_buttons, home_button, link, confirm
from apps.minibot.models import Operator, MiniTemp, Applications


def start_handler(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)
    try:
        oper = Operator.objects.filter(telegram_id=user_id, is_active=True).first()
        if not oper:
            text = f"<strong>ID: </strong>{user_id}\n"
            update.message.reply_html(text)
            return
        try:
            obj = MiniTemp.objects.get(operator=oper)
            obj.step = 0
            obj.save()
        except:
            MiniTemp.objects.create(operator=oper, step=0)
        update.message.reply_html("Начать", reply_markup=main_buttons)
        return
    except Exception as e:
        print(e)


def core(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    oper = Operator.objects.filter(telegram_id=user_id, is_active=True).first()
    try:
        msg = update.message.text
        step = MiniTemp.objects.get(operator=oper)
        if step.step == 0 and msg == 'Начать':
            MiniTemp.objects.filter(operator=oper).update(step=1)
            update.message.reply_html("Введите номер телефона зарегистрированного клиента от @radiusonlinebot ("
                                      "Пример: 991234567)", reply_markup=home_button)
        elif step.step == 1 and not msg == '🏠Главный страница':
            if msg.isnumeric() and len(msg) == 9:
                MiniTemp.objects.filter(operator=oper).update(step=2, phone="998" + msg)
                update.message.reply_html("Введите номер чека или номер договора!", reply_markup=home_button)
            else:
                update.message.reply_html("‼️‼️‼️Введите 9-значный номер телефона(Пример: 991234567)",
                                          reply_markup=home_button)
        elif step.step == 2 and not msg == '🏠Главный страница':
            MiniTemp.objects.filter(operator=oper).update(step=3, order=msg)
            update.message.reply_html("Ссылка на сайт, доказывающая более доступную цену на этот товар в другом"
                                      " магазине!", reply_markup=link)
        elif step.step == 3 and not msg == '🏠Главный страница':
            if msg == "Нет ссылки":
                MiniTemp.objects.filter(operator=oper).update(step=4)
                update.message.reply_html("Изображение того же товара из другого магазина или сайта!",
                                          reply_markup=home_button)
            else:
                MiniTemp.objects.filter(operator=oper).update(step=4, link_other=msg)
                update.message.reply_html("Изображение того же товара из другого магазина или сайта!",
                                          reply_markup=home_button)
        elif step.step == 4 and not msg == '🏠Главный страница':
            photo = update.message.photo
            if not photo:
                update.message.reply_html("‼️‼️‼️Загрузить только фото", reply_markup=home_button)
            else:
                MiniTemp.objects.filter(operator=oper).update(step=5, screen_other=photo[-1].file_id)
                update.message.reply_html("Скриншот цены в 1с!", reply_markup=home_button)
        elif step.step == 5 and not msg == '🏠Главный страница':
            photo = update.message.photo
            if not photo:
                update.message.reply_html("‼️‼️‼️Загрузить только фото", reply_markup=home_button)
            else:
                MiniTemp.objects.filter(operator=oper).update(step=6, screen_radius=photo[-1].file_id)
                text = f"Номер клиента: {step.phone}\nДоговор: {step.order}\n"
                if step.link_other:
                    text += f"Ссылка: {step.link_other}\n"
                text += f"Магазин: {step.operator.shop.shop}\nОператор: {step.operator.full_name}, {step.operator.phone}"
                update.message.reply_html("Скриншот цены в 1с!", reply_markup=home_button)
                context.bot.send_media_group(chat_id=user_id, media=[InputMediaPhoto(f'{step.screen_other}'),
                                                                     InputMediaPhoto(f'{photo[-1].file_id}',
                                                                                     caption=text)])
                update.message.reply_text("Вы подтверждаете вышеизложенное?", reply_markup=confirm)
        elif step.step == 6 and msg == 'Отправить':
            apps = Applications.objects.create(operator=oper, phone=step.phone, order=step.order,
                                               link_other=step.link_other, screen_other=step.screen_other,
                                               screen_radius=step.screen_radius)
            text = f"Номер заявка: {apps.id}\nНомер клиента: {apps.phone}\nДоговор: {apps.order}\n"
            if step.link_other:
                text += f"Ссылка: {apps.link_other}\n"
            text += f"Магазин: {apps.operator.shop.shop}\nОператор: {apps.operator.full_name}, {apps.operator.phone}"
            update.message.reply_html("Скриншот цены в 1с!", reply_markup=home_button)
            context.bot.send_media_group(chat_id=-1002058343693, media=[InputMediaPhoto(f'{apps.screen_other}'),
                                                                        InputMediaPhoto(f'{apps.screen_radius}',
                                                                                        caption=text)])
            MiniTemp.objects.filter(operator=oper).update(step=0, phone=None, order=None, link_other=None,
                                                          screen_other=None, screen_radius=None)
            update.message.reply_html("№1 ✅Запрос отправлен на рассмотрение.", reply_markup=main_buttons)
            update.message.reply_html("Начать", reply_markup=main_buttons)
        elif msg == '🏠Главный страница':
            MiniTemp.objects.filter(operator=oper).update(step=0, phone=None, order=None, link_other=None,
                                                          screen_other=None, screen_radius=None)
            update.message.reply_html("Начать", reply_markup=main_buttons)
    except Exception as e:
        print(e)

