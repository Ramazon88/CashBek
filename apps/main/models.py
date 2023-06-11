from django.db import models

from apps.users.models import *


class Products(models.Model):
    vendor = models.ForeignKey(Vendor_account, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, verbose_name="Дата Добавлена")
    category = models.CharField(max_length=512, default="GSM", verbose_name="Категория")
    model = models.CharField(max_length=512, verbose_name="Модел")
    sku = models.CharField(max_length=512, verbose_name="SKU")
    imei1 = models.CharField(unique=True, max_length=100, verbose_name="IMEI 1")
    imei2 = models.CharField(default="", max_length=100, verbose_name="IMEI 2")
    is_active = models.BooleanField(default=True, verbose_name="Статус")
