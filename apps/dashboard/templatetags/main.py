from django import template

from apps.main.models import Promo, WAIT

register = template.Library()


@register.simple_tag(name="wait")
def count_wait_promo():
    return Promo.objects.filter(status=WAIT).count()
