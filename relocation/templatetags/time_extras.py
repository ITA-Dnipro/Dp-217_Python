from django import template
from dateutil import parser

register = template.Library()


@register.filter
def to_hours_minutes(value):
    time = parser.parse(value).strftime("%H:%M")
    return time

