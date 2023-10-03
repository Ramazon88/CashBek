import json

from django_celery_beat.models import IntervalSchedule, PeriodicTask

from apps.main.utility import get_random_token
from apps.users.models import *

WAIT, ACTIVE, REFUSED, PAUSE, FINISH = (
    "wait",
    "active",
    "refused",
    "pause",
    "finish"
)
choice_promo = (
    (WAIT, "Ожидает одобрения модератором CashBek"),
    (ACTIVE, "Активный"),
    (REFUSED, "Отклоненный"),
    (PAUSE, "Пауза"),
    (FINISH, "Завершенный"),
)

INCOME, EXPENSE = (
    1,
    2
)

choice_cashbek = (
    (INCOME, "Начисление Кэшбэка"),
    (EXPENSE, "Cписание Кэшбэка"),
)


class Products(models.Model):
    ven = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor_account, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, verbose_name="Дата Добавлена")
    model = models.CharField(max_length=512, verbose_name="Модел")
    imei1 = models.CharField(unique=True, max_length=100, verbose_name="IMEI 1")
    sku = models.CharField(max_length=512, verbose_name="SKU")
    is_active = models.BooleanField(default=True, verbose_name="Статус")


class BlackListProducts(models.Model):
    vendor = models.ForeignKey(Vendor_account, on_delete=models.CASCADE)
    model = models.CharField(max_length=512, verbose_name="Модел")
    imei1 = models.CharField(max_length=100, verbose_name="IMEI 1")
    sku = models.CharField(max_length=512, verbose_name="SKU")


class Promo(models.Model):
    ven = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    vendor = models.ForeignKey(Vendor_account, on_delete=models.CASCADE)
    name = models.CharField(max_length=512)
    start = models.DateField()
    end = models.DateField()
    budget = models.IntegerField()
    products = models.ManyToManyField(Products, related_name="promo")
    status = models.CharField(choices=choice_promo, max_length=10, default=WAIT)
    description = models.CharField(max_length=1024, default="")
    who = models.CharField(max_length=1024, default="")
    price_procent = models.IntegerField()


class TempPromo(models.Model):
    vendor = models.ForeignKey(Vendor_account, on_delete=models.CASCADE)
    name = models.CharField(max_length=512)
    start = models.DateField()
    end = models.DateField()
    budget = models.IntegerField()
    products = models.ManyToManyField(Products, related_name="temp_promo")


class PriceProduct(models.Model):
    promo = models.ForeignKey(Promo, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    all_price = models.IntegerField()
    price = models.IntegerField()


class TempPriceProduct(models.Model):
    promo = models.ForeignKey(TempPromo, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.IntegerField()


class QR_code(models.Model):
    qr_id = models.UUIDField(default=uuid.uuid4)
    expiry_date = models.DateTimeField(null=True)
    is_used = models.BooleanField(default=False)
    types = models.IntegerField(choices=choice_cashbek)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    message_id = models.CharField(max_length=100, null=True)
    chat_id = models.CharField(max_length=100, null=True)

    def edit_qr_message(self):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=2,
            period=IntervalSchedule.MINUTES,
        )
        PeriodicTask.objects.create(
            interval=schedule,  # we created this above.
            name=self.qr_id,  # simply describes this periodic task.
            task='apps.main.task.edit_qr_message',  # name of task.
            args=json.dumps([self.chat_id, self.message_id, self.pk]),
            one_off=True
        )

    def save_edit(self, *args, **kwargs):
        super(QR_code, self).save(*args, **kwargs)
        self.edit_qr_message()

    def save(self, *args, **kwargs):
        self.expiry_date = timezone.now() + timedelta(minutes=2)
        super(QR_code, self).save(*args, **kwargs)


class Token_confirm(models.Model):
    token = models.CharField(max_length=16, default=get_random_token)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(SimpleUsers, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    expiry_date = models.DateTimeField(null=True)
    is_used = models.BooleanField(default=False)
    types = models.IntegerField(choices=choice_cashbek)

    def delete_token(self):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=2,
            period=IntervalSchedule.MINUTES,
        )
        PeriodicTask.objects.create(
            interval=schedule,  # we created this above.
            name=f"{self.token}_{self.pk}",  # simply describes this periodic task.
            task='apps.main.task.delete_token',  # name of task.
            args=json.dumps([self.pk]),
            one_off=True
        )

    def save(self, *args, **kwargs):
        self.expiry_date = timezone.now() + timedelta(minutes=2)
        obj = super(Token_confirm, self).save(*args, **kwargs)
        self.delete_token()
        return obj


class Cashbek(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="cash_product")
    promo = models.ForeignKey(Promo, on_delete=models.CASCADE, null=True, blank=True, related_name="cash_promo")
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="cash_vendor")
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="cash_seller")
    user = models.ForeignKey(SimpleUsers, on_delete=models.SET_NULL, null=True, related_name="cash_user")
    price = models.IntegerField()
    amount = models.IntegerField()
    active = models.BooleanField(default=True)
    types = models.IntegerField(choices=choice_cashbek)
    user_phone = models.CharField(blank=True, null=True, max_length=1024)
    description = models.CharField(default="", blank=True, max_length=1024)


class PaymentForSeller(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.BigIntegerField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='payment_seller')
    descriptions = models.CharField(max_length=1024, default="")


class PaymentOfVendor(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.BigIntegerField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='payment_vendor')
    descriptions = models.CharField(max_length=1024, default="")

class Fribase(models.Model):
    fr_id = models.CharField(max_length=256)
    user = models.ForeignKey(SimpleUsers, on_delete=models.CASCADE)


class Notifications(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title_uz = models.CharField(max_length=256)
    title_ru = models.CharField(max_length=256)
    body_uz = models.TextField(max_length=1000)
    body_ru = models.TextField(max_length=1000)
    image = models.ImageField(upload_to="notifications/", blank=True, null=True)


class ReadNot(models.Model):
    user = models.ForeignKey(SimpleUsers, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notifications, on_delete=models.CASCADE, related_name="read")
    read = models.BooleanField(default=False)


class FAQ(models.Model):
    question_uz = models.CharField(max_length=256)
    question_ru = models.CharField(max_length=256)
    answer_uz = models.CharField(max_length=2400)
    answer_ru = models.CharField(max_length=2400)
