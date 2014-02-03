#coding: utf-8

from django import template

register = template.Library()


@register.filter
def join_id(values, text):
    text_return = []
    for val in values:
        text_return.append(str(val.id))

    ret = text.join(text_return)

    return ret