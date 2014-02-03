#coding: utf-8

from apps.portfolio import manages
from apps.users import static
from apps.jevix.jevix import valid_text_jevix
from apps.library import kernel


item_object = manages.Manages()


def is_admin_panel(request):
    if not request.user.is_authenticated():
        return False

    return static.isModels(request.user)


def valid_gallery(data):
    errors = []

    if not data['name'].strip():
        errors.append(u'Ошибка пустое поле загаловок!')

    return data, errors


def valid_item(data, create):
    error = []

    data['text'], error = valid_text_jevix(data['text'])

    if not data['text'].strip():
        error.append(u'Ошибка пустое поле текст!')

    if not data['name'].strip():
        error.append(u'Ошибка пустое поле загаловок!')

    if not data['url'].strip():
        data['url'] = kernel.transliterate(data['name'])

    item = item_object.get_item_url_active([data['url']])
    current = item_object.get_item_id(data['id'])
    if (item and not create) or (item and create and current and item.url != current.url):
        error.append(u'Ошибка токой URL уже существует!')

    return data, error