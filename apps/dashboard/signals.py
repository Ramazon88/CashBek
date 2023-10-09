from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from telegram import Bot

from apps.main.models import Promo, WAIT, ACTIVE, REFUSED
from apps.users.models import Manager
from config.settings import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)


@receiver(pre_save, sender=Promo)
def create_profile(sender, instance, **kwargs):
    try:
        if instance.pk is None:
            info = "<strong>Новое промо</strong>\n\n"
            info += f"<strong>Vendor:</strong> {instance.vendor.vendor.name}({instance.vendor.name})\n"
            info += f"<strong>Имя:</strong> {instance.name}\n"
            info += f"<strong>Дата начала акции:</strong> {instance.start.strftime('%d-%m-%Y')}\n"
            info += f"<strong>Дата окончания акции:</strong> {instance.end.strftime('%d-%m-%Y')}\n"
            info += "<strong>Бюджет:</strong> {:,} Сум\n".format(int(instance.budget))
            info += f"<strong>Статус:</strong> {instance.get_status_display()}\n"
            bot.send_message(chat_id=Manager.objects.all().first().telegram_id, text=info, parse_mode="HTML")
        else:
            old_instance = sender.objects.get(pk=instance.pk)
            info = f"<strong>Vendor:</strong> {instance.vendor.vendor.name}({instance.vendor.name})\n"
            info += f"<strong>Имя:</strong> {instance.name}\n"
            info += f"<strong>Статус:</strong> {instance.get_status_display()}\n"
            info += f"<strong>Комментарий:</strong> {instance.description}\n"
            if old_instance.status != instance.status:
                if old_instance.status == WAIT and instance.status == ACTIVE:
                    bot.send_message(chat_id=Manager.objects.all().first().telegram_id, text="<strong>✅Промо "
                                                                                             "подтверждено</strong>\n\n"
                                                                                             + info, parse_mode="HTML")
                    bot.send_message(chat_id=instance.vendor.telegram_id, text="<strong>✅Промо подтверждено</strong>\n\n" + info, parse_mode="HTML")
                elif old_instance.status == WAIT and instance.status == REFUSED:
                    bot.send_message(chat_id=Manager.objects.all().first().telegram_id, text="<strong>❌Промо "
                                                                                             "отклонено</strong>\n\n" +
                                                                                             info, parse_mode="HTML")
                    bot.send_message(chat_id=instance.vendor.telegram_id, text="<strong>❌Промо отклонено</strong>\n\n" + info, parse_mode="HTML")
                else:
                    bot.send_message(chat_id=-4058643019, text=info, parse_mode="HTML")
                    bot.send_message(chat_id=instance.vendor.telegram_id,
                                     text=info, parse_mode="HTML")
    except Exception as e:
        print(e)

