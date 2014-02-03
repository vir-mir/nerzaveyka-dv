#coding: utf-8

import json
from django.shortcuts import render
from django.http import Http404, HttpResponse
from apps.library import kernel
from apps.portfolio import static
from apps.simplepagination import simple_paginate
from apps.simplepagination import settings
from apps.types_services.static import item_object as services_object


def list_item(request):
    settings.PAGINATION_PER_PAGE = 4

    filter = request.GET['filret'] if request.GET.has_key('filret') else None

    if static.is_admin_panel(request):
        data = static.item_object.get_list_item(filter)
    else:
        data = static.item_object.get_list_item_active(filter)

    data = simple_paginate(data, request, style='digg')

    return render(request, 'portfolio/list_item.html', {
        'is_admin_panel': static.is_admin_panel(request),
        'paginator': data,
    })


def item(request, url):

    data = static.item_object.get_item_url_active(url)

    if not data:
        raise Http404

    data.count_views += 1
    data.save()

    return render(request, 'portfolio/item.html', {
        'item': data,
        'is_admin_panel': static.is_admin_panel(request),
    })


def to_form_add_item(request, id):
    return render(request, 'portfolio/admin/form/add_item.html', {
        'data': [],
        'function_event': 'set_to_form_add_item',
        'errors': [],
        'is_admin_panel': static.is_admin_panel(request),
        })


def aply_gallery(request, id):

    id = id.strip(u'gallery_').split('_')

    gallery_id = int(id[0])
    image_id = int(id[1])

    static.item_object.update_gallery_main_image(gallery_id, image_id)

    return HttpResponse(json.dumps({'text': u'Обложка выбранна!', 'style': u'success'}))


def delete_gallery(request, id):
    static.item_object.delete_gellery_id(id)

    return HttpResponse(json.dumps({'text': u'Галлерея удолена!', 'style': u'success'}))


def delete_image(request, id):

    id = id.strip(u'image_')

    image_id = int(id)

    static.item_object.delete_image_id(image_id)

    return HttpResponse(json.dumps({'text': u'Картинка удолена!', 'style': u'success'}))


def delete_item(request, id):

    static.item_object.delete_item_id(id)

    return HttpResponse(json.dumps({'text': u'Статья удолена!', 'style': u'success'}))


def to_form_edit_item(request, id):
    data = static.item_object.get_item_id(id)
    type_services = services_object.get_items()
    all_items_portfolio = services_object.get_all_items_portfolio(id)

    return render(request, 'portfolio/admin/form/add_item.html', {
        'data': data,
        'all_items_portfolio': all_items_portfolio,
        'type_services': type_services,
        'function_event': 'set_to_form_edit_item',
        'errors': [],
        'is_admin_panel': static.is_admin_panel(request),
        })


def to_form_add_gallery(request, id):

    return render(request, 'portfolio/admin/form/add_gallery.html', {
        'data': [],
        'id_item': id,
        'function_event': 'set_to_form_add_gallery',
        'errors': [],
        'is_admin_panel': static.is_admin_panel(request),
        })


def to_form_edit_gallery(request, id):

    data = static.item_object.get_gallery_id(id)

    return render(request, 'portfolio/admin/form/add_gallery.html', {
        'data': data,
        'id_item': 0,
        'function_event': 'set_to_form_edit_gallery',
        'errors': [],
        'is_admin_panel': static.is_admin_panel(request),
        })


def set_to_form_add_gallery(request, id):
    data = request.POST.copy()
    errors = []

    id_item = data['id_item']

    function_event = 'set_to_form_add_gallery'
    style = 'danger'

    errors = []
    data, errors = static.valid_gallery(data.copy())

    if len(errors) == 0:
        data = static.item_object.insert_gallery(data, id_item)
        style = 'success'
        function_event = 'set_to_form_edit_gallery'
        errors.append(u'Галлерея успешно созданна')

    return render(request, 'portfolio/admin/form/add_gallery.html', {
        'data': data,
        'id_item': id_item,
        'function_event': function_event,
        'errors': errors,
        'style': style,
        'is_admin_panel': static.is_admin_panel(request),
        })


def set_to_form_edit_gallery(request, id):
    data = request.POST.copy()
    errors = []

    function_event = 'set_to_form_edit_gallery'
    style = 'danger'
    id_item = data['id_item'] if data.has_key('id_item') else 0
    errors = []
    data, errors = static.valid_gallery(data.copy())

    if len(errors) == 0:
        data = static.item_object.update_gallery(data)
        style = 'success'
        errors.append(u'Галлерея успешно отредактированна')

    return render(request, 'portfolio/admin/form/add_gallery.html', {
        'data': data,
        'id_item': id_item,
        'function_event': function_event,
        'errors': errors,
        'style': style,
        'is_admin_panel': static.is_admin_panel(request),
        })


def set_to_form_add_item(request, id):
    data = request.POST.copy()
    type_services = services_object.get_items()
    data['id'] = int(data['id'])
    data['seo_id'] = int(data['seo_id'])

    all_items_portfolio = services_object.get_all_items_portfolio(data['id'])

    errors = []
    data, errors = static.valid_item(data.copy(), False)

    style = 'danger'
    function_event = 'set_to_form_add_item'
    if len(errors) == 0:
        data = static.item_object.insert_item(data)
        style = 'success'
        function_event = 'set_to_form_edit_item'
        errors.append(u'Услуга успешно созданна')

    return render(request, 'portfolio/admin/form/add_item.html', {
        'data': data,
        'type_services': type_services,
        'all_items_portfolio': all_items_portfolio,
        'function_event': function_event,
        'errors': errors,
        'style': style,
        'is_admin_panel': static.is_admin_panel(request),
        })


def set_to_form_edit_item(request, id):
    data = request.POST.copy()
    data['id'] = int(data['id'])
    type_services = services_object.get_items()
    all_items_portfolio = services_object.get_all_items_portfolio(data['id'])
    data['seo_id'] = int(data['seo_id'])

    errors = []
    data, errors = static.valid_item(data.copy(), True)
    post = data.copy()
    style = 'danger'
    function_event = 'set_to_form_edit_item'
    if len(errors) == 0:
        data = static.item_object.update_item(data)
        if int(post['seo_id']) > 0:
            data = static.item_object.update_seo_item(post)
        elif post['title'].strip() or post['keywords'].strip() or post['description'].strip():
            data = static.item_object.insert_seo_item(post)

        style = 'success'
        function_event = 'set_to_form_edit_item'
        errors.append(u'Услуга успешно отредактирована')

    return render(request, 'portfolio/admin/form/add_item.html', {
        'data': data,
        'type_services': type_services,
        'all_items_portfolio': all_items_portfolio,
        'function_event': function_event,
        'errors': errors,
        'style': style,
        'is_admin_panel': static.is_admin_panel(request),
        })


def controller(request, url):
    urls = kernel.get_url_list(url)

    if not urls:
        return list_item(request)

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

    return item(request, urls)