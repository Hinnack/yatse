# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from yatse.models import Server

@admin.register(Server)
class yatsAdmin(admin.ModelAdmin):
    exclude = ('c_date', 'c_user', 'u_user', 'u_date', 'd_user', 'd_date', 'active_record')
    list_filter = ('active_record',)

    def save_model(self, request, obj, form, change):
        obj.save(user=request.user)

    def delete_model(self, request, obj):
        obj.delete(user=request.user)

    """
    def changelist_view(self, request, extra_context=None):

        if not request.GET.has_key('active_record__exact'):
            q = request.GET.copy()
            q['active_record__exact'] = 'N'
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()
        return super(yatsAdmin, self).changelist_view(request, extra_context=extra_context)
    """
