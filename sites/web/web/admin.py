# -*- coding: utf-8 -*-
from django.contrib import admin
from models import ticket_component
from yatse.admin import yatseAdmin

admin.site.register(ticket_component, yatseAdmin)
