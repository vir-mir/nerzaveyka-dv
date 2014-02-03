#coding: utf-8

import re

from django import template

register = template.Library()


@register.filter(name='replace_cut')
def replace_cut(values):
    values = re.sub(r'(?isu)\[vir-mir\s*(name=[\'"].*[\'"])?\s*\]', '', values)

    return values

@register.filter(name='replace_cut_post')
def replace_cut_post(values, id):

    cut = re.match(r'(?isu).*\[vir-mir\s*name=[\'"](.*)[\'"]\s*\]', values)
    if not cut:
        cut = u'Читать дальше >>>'
    else:
        cut = cut.group(1)

    cut = u'<a href="/portfolio/%s/" class="btn pull-right btn-danger">%s</a><div class="clearfix"></div>' % (id, cut)
    values = re.sub(r'(?isu)\[vir-mir\s*(name=[\'"].*[\'"])?\s*\].*', cut, values)

    return values