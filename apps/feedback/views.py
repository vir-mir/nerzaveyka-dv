#coding: utf-8

import json
from django.http import Http404, HttpResponse
from apps.library import kernel
from apps.feedback import static


def send_fos(request, id):

    errors, data = static.valid_fos(request.POST.copy())

    if len(errors) > 0:
        style = u'danger'
        text = errors
        error = 0
    else:
        style = u'success'
        text = [u'Сообщение успешно отправлено, с вами свяжется наш специалист!']
        error = 1
        static.item_object.insert_fos(data)
        static.send_mail_fos(data)

    return HttpResponse(json.dumps({'text': text, 'style': style, 'error': error}))


def send_callback(request, id):

    errors, data = static.valid_callback(request.POST.copy())

    if len(errors) > 0:
        style = u'danger'
        text = errors
        error = 0
    else:
        style = u'success'
        text = [u'Сообщение успешно отправлено, с вами свяжется наш специалист!']
        error = 1
        static.item_object.insert_callback(data)
        static.send_mail_callback(data)

    return HttpResponse(json.dumps({'text': text, 'style': style, 'error': error}))


def controller(request, url):
    urls = kernel.get_url_list(url)

    if urls[0] == 'ajax':
        try:
            fun = request.GET['function_event']
        except:
            fun = request.POST['function_event']

        try:
            id = request.GET['id']
        except:
            try:
                id = request.POST['id']
            except:
                id = 0

        return globals()[fun](request, id)

    raise Http404
