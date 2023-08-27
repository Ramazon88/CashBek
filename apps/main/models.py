import json

from django_celery_beat.models import IntervalSchedule, PeriodicTask

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

choice_cashbek = (
    (1, "Начисление Кэшбэка"),
    (2, "Cписание Кэшбэка"),
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
    price = models.IntegerField()


class TempPriceProduct(models.Model):
    promo = models.ForeignKey(TempPromo, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.IntegerField()


class QR_code(models.Model):
    qr_id = models.UUIDField(default=uuid.uuid4)
    expiry_date = models.DateTimeField(null=True)
    is_used = models.BooleanField(default=False)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
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


class Cashbek(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    user = models.ForeignKey(SimpleUsers, on_delete=models.CASCADE)
    amount = models.IntegerField()
    active = models.BooleanField(default=True)
    types = models.IntegerField(choices=choice_cashbek)
