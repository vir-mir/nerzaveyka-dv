#coding: utf-8

from django.db import models


class Fos(models.Model):
    fio = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)


class Callback(models.Model):
    fio = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)