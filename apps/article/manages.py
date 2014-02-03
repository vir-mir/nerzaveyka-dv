#coding: utf-8

import datetime
import os
from nerzaveyka import settings
from apps.article.models import Item, Seo, Gallery, Image


class Manages():

    def get_list_item_active(self):
        return Item.objects.order_by('-dd_creation').filter(active=1)

    def get_list_item(self):
        return Item.objects.order_by('-dd_creation').filter()

    def get_list_item_slide(self, count):
        return Item.objects.order_by('?').filter(active=1, gallery__active=0)[:count]

    def get_item_url_active(self, url):
        url = url[0]

        try:
            return Item.objects.get(active=1, url=url)
        except Item.DoesNotExist:
            return None

    def get_image_id(self, id):
        try:
            return Image.objects.get(id=id)
        except Item.DoesNotExist:
            return None

    def get_item_id(self, id):
        try:
            return Item.objects.get(id=id)
        except Item.DoesNotExist:
            return None

    def insert_gallery(self, data, id_item):

        gallery = Gallery()
        item = self.get_item_id(id_item)

        gallery.height = data['height']
        gallery.height_prev = data['height_prev']
        gallery.width = data['width']
        gallery.width_prev = data['width_prev']
        gallery.name = data['name']

        if not data.has_key('ratio'):
            gallery.ratio = 0
        else:
            gallery.ratio = 1

        if not data.has_key('active'):
            gallery.active = 0
        else:
            gallery.active = 1

        gallery.save()

        item.gallery.add(gallery)

        return gallery

    def insert_gallery_images(self, src, src_small, id):
        image = Image()
        gallery = self.get_gallery_id(id)

        image.src = src
        if src_small:
            image.src_small = src_small

        image.save()
        gallery.images.add(image)

    def update_gallery_main_image(self, gallery_id, image_id):
        gallery = self.get_gallery_id(gallery_id)
        gallery.main_image_id = image_id
        gallery.save()
        return gallery

    def delete_image_id(self, id):
        image = self.get_image_id(id)
        src = settings.MEDIA_ROOT + image.src
        src_small = settings.MEDIA_ROOT + image.src_small
        os.remove(src)
        os.remove(src_small)
        image.delete()

    def delete_gellery_id(self, id):
        gallery = self.get_gallery_id(id)
        imgs = gallery.images.all()
        if imgs:
            for im in imgs:
                self.delete_image_id(im.id)
        gallery.delete()

    def delete_item_id(self, id):
        item = self.get_item_id(id)
        imgs = item.gallery.all()
        if  imgs:
            for im in imgs:
                self.delete_gellery_id(im.id)
        item.delete()

    def update_gallery(self, data):

        gallery = self.get_gallery_id(data['id'])

        gallery.height = data['height']
        gallery.height_prev = data['height_prev']
        gallery.width = data['width']
        gallery.width_prev = data['width_prev']
        gallery.name = data['name']

        if not data.has_key('ratio'):
            gallery.ratio = 0
        else:
            gallery.ratio = 1

        if not data.has_key('active'):
            gallery.active = 0
        else:
            gallery.active = 1

        gallery.save()

        return gallery

    def get_gallery_id(self, id):
        try:
            return Gallery.objects.get(id=id)
        except Item.DoesNotExist:
            return None

    def get_gallery_item_id(self, id):
        item = self.get_item_id(id)
        return item.gallery.all()

    def update_item(self, data):
        item = self.get_item_id(data['id'])

        item.count_views = data['count_views']
        item.name = data['name']
        item.url = data['url']
        item.text = data['text']
        item.order = data['order']

        if not data.has_key('active'):
            item.active = 0
        else:
            item.active = 1

        if not data.has_key('gallery_is_item'):
            item.gallery_is_item = 0
        else:
            item.gallery_is_item = 1

        item.save()

        return item

    def insert_seo_item(self, data):
        item = self.get_item_id(data['id'])
        seo = Seo()

        if data['description'].strip():
            seo.description = data['description']
        if data['keywords'].strip():
            seo.keywords = data['keywords']
        if data['title'].strip():
            seo.title = data['title']

        seo.save()
        item.seo_id = seo.id
        item.save()

        return item

    def update_seo_item(self, data):
        item = self.get_item_id(data['id'])

        if data['description'].strip():
            item.seo.description = data['description']
        if data['keywords'].strip():
            item.seo.keywords = data['keywords']
        if data['title'].strip():
            item.seo.title = data['title']

        item.seo.save()

        return item

    def insert_item(self, data):

        item = Item()

        item.count_views = data['count_views']
        item.name = data['name']
        item.url = data['url']
        item.text = data['text']
        item.order = data['order']

        if not data.has_key('active'):
            item.active = 0
        else:
            item.active = 1

        if not data.has_key('gallery_is_item'):
            item.gallery_is_item = 0
        else:
            item.gallery_is_item = 1

        item.dd_creation = datetime.datetime.now()

        item.save()

        return item

