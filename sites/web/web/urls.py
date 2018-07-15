# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from simple_sso.sso_server.server import Server
#from yatse.login import password_reset_form

admin.autodiscover()
test_server = Server()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),  # NOQA
    # url(r'^', include('yatse.check.urls')),
    url(r'^server/', include(test_server.get_urls())),
    url('^', include('django.contrib.auth.urls')),
    url(r'^', include('yatse.urls')),
]

urlpatterns += staticfiles_urlpatterns()
