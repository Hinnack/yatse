# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from yatse.views import root

urlpatterns = [
   url(r'^$',
        view=root,
        name='view_root'),
]
