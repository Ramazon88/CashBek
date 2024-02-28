from django.db import models


class Shop(models.Model):
    shop = models.CharField(max_length=30)

    def __str__(self):
        return self.shop

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"


class Operator(models.Model):
    full_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="Магазин")
    telegram_id = models.BigIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name


class MiniTemp(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.SET_NULL, blank=True, null=True)
    step = models.IntegerField()
    phone = models.CharField(max_length=100, null=True, blank=True)
    order = models.CharField(max_length=100, null=True, blank=True)
    link_other = models.CharField(max_length=512, null=True, blank=True)
    screen_other = models.CharField(max_length=256, null=True, blank=True)
    screen_radius = models.CharField(max_length=256, null=True, blank=True)


class Applications(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.SET_NULL, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    order = models.CharField(max_length=100, null=True, blank=True)
    link_other = models.CharField(max_length=512, null=True, blank=True)
    screen_other = models.CharField(max_length=256, null=True, blank=True)
    screen_radius = models.CharField(max_length=256, null=True, blank=True)
