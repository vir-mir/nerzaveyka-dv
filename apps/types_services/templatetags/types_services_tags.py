#coding: utf-8

from django import template
from apps.types_services import views

register = template.Library()


@register.inclusion_tag('types_services/main.html', takes_context=True)
def main_types_services_fn(context, request):

    return views.main(request)