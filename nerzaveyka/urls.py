from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

handler404 = 'apps.site.views.error_404'

urlpatterns = patterns('')

urlpatterns = patterns('',
    # index:
    url(r'^$', 'apps.site.views.index', name='index'),

    url(r'^company/$', 'apps.site.views.company', name='company'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # models url:
    url(r'^article/(?P<url>.*)$', 'apps.article.views.controller'),
    url(r'^portfolio/(?P<url>.*)$', 'apps.portfolio.views.controller'),
    url(r'^types_services/(?P<url>.*)$', 'apps.types_services.views.controller'),
    url(r'^feedback/(?P<url>.*)$', 'apps.feedback.views.controller'),
    url(r'^uploads/(?P<module>\w+)/(?P<id>\d+)/$', 'apps.upload.views.controller'),


) 


if settings.DEBUG:
    urlpatterns += patterns(
        '',
       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )


urlpatterns += staticfiles_urlpatterns()