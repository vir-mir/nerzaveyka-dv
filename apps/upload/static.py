#coding: utf-8

from apps.article import manages as art
from apps.portfolio import manages as port


def get_module(module):
    if module == 'article':
        return art.Manages()
    elif module == 'portfolio':
        return port.Manages()