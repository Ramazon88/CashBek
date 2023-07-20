from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.main.models import Promo


# @receiver(post_save, sender=Promo)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#
