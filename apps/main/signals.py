from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.main.task import create_read, Notifications


@receiver(post_save, sender=Notifications)
def create_profile(sender, instance, created, **kwargs):
    if created:
        create_read.delay(instance.pk)




