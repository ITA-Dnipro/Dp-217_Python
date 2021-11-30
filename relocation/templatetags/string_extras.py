from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter
@stringfilter
def left_strip(value, arg=' '):
    return value.lstrip(arg)


@register.filter
@stringfilter
def right_strip(value, arg=' '):
    return value.rstrip(arg)


@register.filter
@stringfilter
def erase(value, arg):
    return value.replace(arg, '')
