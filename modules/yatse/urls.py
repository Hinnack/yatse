# -*- coding: utf-8 -*-
from django.conf.urls import url
from yatse.views import root, search, info, show_board, board_by_id, next_board, reports, redirectToTicket, api

urlpatterns = [
   url(r'tickets/(?P<serverID>\d+)/(?P<ticketID>\d+)/$',
       view=redirectToTicket,
       name='redirectToTicket'),

   url(r'tickets/api/(?P<serverID>\d+)/(?P<ticketID>\d+)/$',
       view=api,
       name='api'),

   url(r'tickets/search/$',
       view=search,
       name='search'),

   url(r'info/$',
       view=info,
       name='info'),

   url(r'^$',
       view=root,
       name='view_root'),

   # reports
   url(r'^reports/$',
       view=reports,
       name='reports'),

   # boards
   url(r'^board/(?P<id>\d+)/$',
       view=board_by_id,
       name='board_by_id'),

   url(r'^board/(?P<name>[\w|\W]+)/$',
       view=show_board,
       name='board_by_name'),

   url(r'^board/$',
       view=next_board,
       name='next_board'),
]
