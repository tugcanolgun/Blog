from panel.models import Static
from django import template

register = template.Library()

@register.simple_tag()
def all_statics():
    context = Static.objects.all()
    return context
