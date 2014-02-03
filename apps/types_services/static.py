#coding: utf-8

from apps.types_services import manages
from apps.users import static

item_object = manages.Manages()


def is_admin_panel(request):
    if not request.user.is_authenticated():
        return False

    return static.isModels(request.user)


def valid_item(data):
    errors = []

    if not data['name'].strip():
        errors.append(u'Ошибка пустое поле загаловок!')

    return data, errors