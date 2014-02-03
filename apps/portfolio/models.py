#coding: utf-8

from django.db import models


class Image(models.Model):
    alt = models.CharField(max_length=255, null=True, blank=True)
    src = models.CharField(max_length=255)
    src_small = models.CharField(max_length=255, null=True, blank=True)


class Gallery(models.Model):
    name = models.CharField(max_length=255)
    ratio = models.SmallIntegerField(max_length=2, null=True, blank=True)
    active = models.SmallIntegerField(max_length=2, null=True, blank=True)
    width_prev = models.IntegerField(max_length=11, null=True, blank=True)
    height_prev = models.IntegerField(max_length=11, null=True, blank=True)
    width = models.IntegerField(max_length=11, null=True, blank=True)
    height = models.IntegerField(max_length=11, null=True, blank=True)
    images = models.ManyToManyField(Image, null=True, blank=True, related_name='images')
    main_image = models.ForeignKey(Image, null=True, blank=True, related_name='main_image')


class Seo(models.Model):
    keywords = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)


class Item(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    text = models.TextField()
    active = models.IntegerField(max_length=2)
    gallery_is_item = models.IntegerField(max_length=2, null=True, blank=True)
    dd_creation = models.DateTimeField()
    count_views = models.IntegerField(max_length=11, blank=True)
    order = models.IntegerField(max_length=11, blank=True)
    gallery = models.ManyToManyField(Gallery, null=True, blank=True)
    seo = models.OneToOneField(Seo, null=True, blank=True)
