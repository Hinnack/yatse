# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),  # NOQA
    #url(r'^', include('yatse.check.urls')),
    url(r'^', include('yatse.urls')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

urlpatterns += staticfiles_urlpatterns()
