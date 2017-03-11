from django import template
from django.utils.safestring import mark_safe
from ..models import UserText

register = template.Library()

@register.simple_tag
def tag(name):
    try:
        return mark_safe(UserText.objects.get(tag=name).text)
    except:
        return "<<{}>>".format(name)
