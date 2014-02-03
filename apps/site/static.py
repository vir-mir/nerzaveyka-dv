#coding: utf-8

from apps.users import static


def is_admin_panel(request):
    if not request.user.is_authenticated():
        return False

    return static.isModels(request.user)