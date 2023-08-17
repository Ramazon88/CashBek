from django.db import models


class SellerTemp(models.Model):
    tg_id = models.CharField(max_length=100)
    step = models.IntegerField()
    qr_type = models.IntegerField(null=True)
    imei = models.CharField(max_length=100, null=True, blank=True)