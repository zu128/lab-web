from django import template
import markdown
from django.utils.safestring import mark_safe
from django.utils import dateformat
register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg


@register.filter()
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))


@register.filter()
def date(value):
    return dateformat.format(value, 'Y.m.d')


@register.filter()
def board_name(value):
    if value == 'notice':
        return '공지사항'
    elif value == 'data':
        return '자료실'
    else:
        return '게시판'

