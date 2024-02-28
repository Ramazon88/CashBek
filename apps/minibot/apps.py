from django.apps import AppConfig


class MinibotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.minibot'

    def ready(self):
        from .dispatcher import ready
        ready()