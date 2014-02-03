#coding: utf-8

def CallbackTagLs(tag, resParams, content):
    html = u"""
        <i class="icon-user"></i> <a href="/users/info/%s/">%s</a>
    """ % (resParams['user'], resParams['user'])
    return html
