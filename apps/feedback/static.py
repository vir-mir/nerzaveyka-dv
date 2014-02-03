# -- coding: utf-8 --

from django.template import loader, Context
from apps.feedback import manages
from apps.users import static
from django.shortcuts import render
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core import mail
import base64
import locale
enc = locale.getpreferredencoding()

item_object = manages.Manages()


def email(value):
    try:
        validate_email(value)
        return True

    except (ValidationError), e:
        return False


def is_admin_panel(request):
    if not request.user.is_authenticated():
        return False

    return static.isModels(request.user)


def send_mail_fos(data):

    text = loader.get_template('fos/email_html.html')
    text = text.render(Context({
        'text': data['text'].replace('\r', '').replace('\n', '<br>'),
        'fio': data['fio']
    }))

    email = mail.EmailMessage(
        u"Вопрос с сайта nerzaveyka-dv.ru",
        text,
        data['email'],
        ['info+fos@nerzaveyka-dv.ru']
    )
    fio = data['fio'].encode('utf-8').encode('base64').strip('\n')
    email.extra_headers = {'From': u"=?UTF-8?B?%s?= <%s>" % (fio, data['email'])}
    email.content_subtype = 'html'
    email.send()


def send_mail_callback(data):

    text = loader.get_template('fos/callback_html.html')
    text = text.render(Context({
        'text': data['text'].replace('\r', '').replace('\n', '<br>'),
        'fio': data['fio'],
        'phone': data['phone'],
    }))

    email = mail.EmailMessage(
        u"Вопрос с сайта nerzaveyka-dv.ru",
        text,
        data['email'] if data['email'].strip() else 'info@nerzaveyka-dv.ru',
        ['info+callback@nerzaveyka-dv.ru']
    )
    fio = data['fio'].encode('utf-8').encode('base64').strip('\n')
    email.extra_headers = {'From': u"=?UTF-8?B?%s?= <%s>" % (fio, data['email'])}
    email.content_subtype = 'html'
    email.send()


def valid_fos(data):
    errors = []

    if not data['fio'].strip():
        errors.append(u'Ошибка пустое поле Ф.И.О!')

    if not email(data['email']):
        errors.append(u'Введите правильный адрес электронной почты!')

    if not data['text'].strip():
        errors.append(u'Ошибка пустое поле Текст!')


    return errors, data


def valid_callback(data):
    errors = []

    if not data['fio'].strip():
        errors.append(u'Ошибка пустое поле Ф.И.О!')

    if data['email'].strip() and not email(data['email']):
        errors.append(u'Введите правильный адрес электронной почты!')

    if not data['phone'].strip():
        errors.append(u'Ошибка пустое поле Телефон!')

    if not data['text'].strip():
        errors.append(u'Ошибка пустое поле Текст!')


    return errors, data