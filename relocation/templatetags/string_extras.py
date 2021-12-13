import urllib.parse

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


@register.filter
@stringfilter
def encode_to_url(value):
    return urllib.parse.quote_plus(value)


@register.filter
@stringfilter
def replace(value, arg):
    """
    Usage:
    {{ "abc"|replace:"a|b" }}
    """
    args = arg.split('|')
    if len(arg.split('|')) != 2:
        return value

    return value.replace(args[0], args[1])

