#coding: utf-8

import json
from django.shortcuts import render
from django.http import Http404, HttpResponse
from apps.library import kernel
from apps.types_services import static
from apps.portfolio.static import item_object


def main(request):

    list_services = static.item_object.get_items()

    return {
        'is_admin_panel': static.is_admin_panel(request),
        'list_services': list_services,
    }


def to_form_add_item(request, id):

    portfolios = item_object.get_list_item()

    return render(request, 'types_services/admin/form/add_item.html', {
        'data': [],
        'portfolios': portfolios,
        'function_event': 'set_to_form_add_item',
        'errors': [],
        'is_admin_panel': static.is_admin_panel(request),
        })


def get_is_to(data):
    datas = []
    for d in data.portfolios.all():
        datas.append(d.id)

    return datas


def to_form_edit_item(request, id):

    data = static.item_object.get_item_id(id)

    portfolios = item_object.get_list_item()



    return render(request, 'types_services/admin/form/add_item.html', {
        'data': data,
        'curents': get_is_to(data),
        'portfolios': portfolios,
        'function_event': 'set_to_form_edit_item',
        'errors': [],
        'is_admin_panel': static.is_admin_panel(request),
        })


def delete_item(request, id):
    static.item_object.delete_item_id(id)
    return HttpResponse(json.dumps({'text': u'Услуга удолена!', 'style': u'success'}))


def set_to_form_add_item(request, id):
    data = request.POST.copy()

    data['id'] = int(data['id'])

    portfolios = item_object.get_list_item()

    errors = []
    data, errors = static.valid_item(data.copy())

    if data.has_key('portfolios') and data['portfolios'].strip(', '):
        data['data'] = data['portfolios'].strip(', ').split(',')
    else:
        data['data'] = []

    style = 'danger'
    function_event = 'set_to_form_add_item'
    if len(errors) == 0:
        data = static.item_object.insert_item(data)
        style = 'success'
        function_event = 'set_to_form_edit_item'
        errors.append(u'Статья успешно созданна')

    return render(request, 'types_services/admin/form/add_item.html', {
        'data': data,
        'function_event': function_event,
        'portfolios': portfolios,
        'curents': get_is_to(data),
        'errors': errors,
        'style': style,
        'is_admin_panel': static.is_admin_panel(request),
        })


def set_to_form_edit_item(request, id):
    data = request.POST.copy()

    errors = []

    if data.has_key('portfolios') and data['portfolios'].strip(', '):
        data['data'] =  data['portfolios'].strip(', ').split(',')
    else:
        data['data'] = []

    portfolios = item_object.get_list_item()

    data['id'] = int(data['id'])


    data, errors = static.valid_item(data.copy())
    post = data.copy()
    style = 'danger'
    function_event = 'set_to_form_edit_item'
    if len(errors) == 0:
        data = static.item_object.update_item(data)
        style = 'success'
        function_event = 'set_to_form_edit_item'
        errors.append(u'Статья успешно отредактирована')

    return render(request, 'types_services/admin/form/add_item.html', {
        'data': data,
        'function_event': function_event,
        'portfolios': portfolios,
        'curents': get_is_to(data),
        'errors': errors,
        'style': style,
        'is_admin_panel': static.is_admin_panel(request),
        })


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
