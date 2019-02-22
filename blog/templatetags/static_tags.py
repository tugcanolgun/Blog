from panel.models import Static
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag()
def all_statics():
    context = Static.objects.all()
    return context

@register.simple_tag()
def blog_name():
    context = settings.DISPLAY_NAME
    return context
