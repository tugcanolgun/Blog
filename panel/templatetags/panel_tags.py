from panel.models import Category
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag()
def all_categories():
    context = Category.objects.all()
    return context


@register.simple_tag()
def blog_name():
    context = settings.DISPLAY_NAME
    return context
