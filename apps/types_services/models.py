#coding: utf-8

from django.db import models
from apps.portfolio.models import Item as Item_portfolio


class Item(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    portfolios = models.ManyToManyField(Item_portfolio, null=True, blank=True)