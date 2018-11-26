import re

from django import template


register = template.Library()

@register.filter
def divide(value, args):
    try:
        a = int(len(re.sub('<[^<]+?>', '', value))) / int(args)
        return int(a)
    except (ValueError, ZeroDivisionError):
        return None
