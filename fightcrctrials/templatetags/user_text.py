from django import template
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags
from ..models import UserText

register = template.Library()

@register.simple_tag
def tag(name):
    try:
        return mark_safe(UserText.objects.get(tag=name).text)
    except:
        return "<<{}>>".format(name)

@register.simple_tag
def tag_stripped(name):
    try:
        return strip_tags(UserText.objects.get(tag=name).text)
    except:
        return "<<{}>>".format(name)
