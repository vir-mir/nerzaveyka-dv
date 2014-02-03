#coding: utf-8

from django.shortcuts import render
from apps.site import static


def index(request):
    return render(request, 'site/index.html', {'is_admin_panel': static.is_admin_panel(request)})


def company(request):
    return render(request, 'site/company.html', {'is_admin_panel': static.is_admin_panel(request)})


def error_404(request):
    return render(request, 'errors/404.html', {'is_admin_panel': static.is_admin_panel(request)})