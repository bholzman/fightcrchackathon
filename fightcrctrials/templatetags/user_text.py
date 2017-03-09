from django import template
from ..models import UserText

register = template.Library()

@register.simple_tag
def tag(name):
    try:
        return UserText.objects.get(tag=name).text
    except:
        return "<<{}>>".format(name)
