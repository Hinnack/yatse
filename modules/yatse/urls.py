# -*- coding: utf-8 -*-
from django.conf.urls import url
from yatse.views import root, search, info

urlpatterns = [
   url(r'tickets/search/$',
       view=search,
       name='search'),

   url(r'info/$',
       view=info,
       name='info'),

   url(r'^$',
       view=root,
       name='view_root'),
]
