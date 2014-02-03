#coding: utf-8

import os
from django.http import HttpResponse
from apps.upload import static
from apps.library import kernel
from random import randint
from nerzaveyka import settings
from django.views.decorators.csrf import csrf_exempt
from PIL import Image, ImageOps
import random


@csrf_exempt
def controller(request, module, id):
    if request.FILES.has_key('Filedata'):
        typeFile = ['.jpg', '.jpeg','.gif','.png']
        dataFile = os.path.splitext(request.FILES['Filedata'].name)[1]
        if dataFile in typeFile:
            img = handle_uploaded_file(request.FILES['Filedata'], id, module)
            return HttpResponse(u'file:%s' % img)
        else:
            return HttpResponse(u'Неверный тип файла!')
    else:
        return HttpResponse(u'Ощибка вставки! Только для авторизованных!')


def set_na_file(dir, name):

    if os.path.exists(os.path.join(dir, name)):

        ex = os.path.splitext(name)[1]
        name = u"%s_%s%s" % (name, randint(0, 99999), ex)
        return set_na_file(dir, name)
    else:
        return name


def handle_uploaded_file(f, id_module, module):

    big_img = u'/%s/%s/' % (module, id_module)
    small_img = u'/%s/%s/' % (module, id_module)

    path = os.path.join(settings.MEDIA_ROOT, u"%s" % module)

    if not os.path.isdir(path):
        os.mkdir(path, 0777)

    path = os.path.join(path, u"%s" % id_module)

    if not os.path.isdir(path):
        os.mkdir(path, 0777)

    file_os = os.path.join(path, kernel.transliterate(f.name)).lower()

    if os.path.exists(file_os):
        os.remove(file_os)

    destination = open(file_os, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

    module_object = static.get_module(module)

    gallery = module_object.get_gallery_id(id_module)

    if gallery:
        if gallery.ratio == 1:
            pref = u"%s_%s_" % (gallery.images.count(), random.randrange(0, 99999))
            width = int(gallery.width) if int(gallery.width) > 0 else 99999999999999999
            height = int(gallery.height) if int(gallery.height) > 0 else 99999999999999999
            image = Image.open(file_os)
            image.thumbnail((width, height), Image.ANTIALIAS)
            ex = os.path.splitext(file_os)[-1]
            big = os.path.join(path, (u"%sbig%s" % (pref, ex))).lower()
            big_img += u"%sbig%s" % (pref, ex)
            if os.path.exists(big):
                os.remove(big)
            image.save(big)

            width = int(gallery.width_prev) if int(gallery.width_prev) > 0 else 99999999999999999
            height = int(gallery.height_prev) if int(gallery.height_prev) > 0 else 99999999999999999
            img = Image.open(big)
            img.thumbnail((width, height), Image.ANTIALIAS)
            small = os.path.join(path, (u"%ssmall%s" % (pref, ex))).lower()
            small_img += u"%ssmall%s" % (pref, ex)
            if os.path.exists(small):
                os.remove(small)
            img.save(small)

        else:
            pref = u"%s_%s_" % (gallery.images.count(), random.randrange(0, 99999))
            width = int(gallery.width) if int(gallery.width) > 0 else 99999999999999999
            height = int(gallery.height) if int(gallery.height) > 0 else 99999999999999999
            ex = os.path.splitext(file_os)[-1]
            image = Image.open(file_os)
            imagefit = ImageOps.fit(image, (width, height), Image.ANTIALIAS)
            big = os.path.join(path, (u"%sbig%s" % (pref, ex))).lower()
            big_img += u"%sbig%s" % (pref, ex)
            if os.path.exists(big):
                os.remove(big)
            imagefit.save(big)
            width = int(gallery.width_prev) if int(gallery.width_prev) > 0 else 99999999999999999
            height = int(gallery.height_prev) if int(gallery.height_prev) > 0 else 99999999999999999
            img = Image.open(file_os)
            imgfit = ImageOps.fit(img, (width, height), Image.ANTIALIAS)
            small = os.path.join(path, (u"%ssmall%s" % (pref, ex))).lower()
            small_img += u"%ssmall%s" % (pref, ex)
            if os.path.exists(small):
                os.remove(small)
            imgfit.save(small)

    module_object.insert_gallery_images(big_img, small_img, id_module)

    os.remove(file_os)

    return u'%s/%s' % (settings.MEDIA_URL, f.name)
