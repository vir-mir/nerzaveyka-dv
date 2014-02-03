#coding: utf-8

from django import template
from apps.article import static

register = template.Library()


@register.inclusion_tag('article/slide.html', takes_context=True)
def slide_article_fn(context, count):

    data = static.item_object.get_list_item_slide(count)

    if not data:
        return {
            'slide_article': []
        }

    newData = []

    for item in data:
        if item.gallery.all()[0].images.count() == 0:
            continue
        img = item.gallery.all()[0].images.all()[0]
        newData.append({'data': item, 'img': img})

    return {
        'slide_article': newData
    }
