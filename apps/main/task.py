from celery import shared_task

from apps.main.models import QR_code
from config.settings import seller_bot


@shared_task(bint=True)
def edit_qr_message(chat_id, message_id, pk):
    seller_bot.delete_message(chat_id=chat_id, message_id=message_id)
    seller_bot.send_message(chat_id=chat_id, text="Срок действия QR-кода истек")
    QR_code.objects.filter(pk=pk).delete()
