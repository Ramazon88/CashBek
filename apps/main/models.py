from apps.users.models import *


class Products(models.Model):
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
    name = models.CharField(max_length=512)
    start = models.DateField()
    end = models.DateField()
    budget = models.IntegerField()
