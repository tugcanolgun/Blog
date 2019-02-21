from panel.models import Categories, Content
from django import template

register = template.Library()

@register.simple_tag()
def all_categories():
    context = Categories.objects.all()
    return context
