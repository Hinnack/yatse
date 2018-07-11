# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

import datetime

class base(models.Model):
    active_record = models.BooleanField(default=True)

    # creation
    c_date = models.DateTimeField(default=datetime.datetime.now)
    c_user = models.ForeignKey(User, related_name='+')
    # update
    u_date = models.DateTimeField(default=datetime.datetime.now)
    u_user = models.ForeignKey(User, related_name='+')
    # deletion'
    d_date = models.DateTimeField(null=True)
    d_user = models.ForeignKey(User, related_name='+', null=True)

    def save(self, *args, **kwargs):
        if 'user' not in kwargs and 'user_id' not in kwargs:
            raise Exception('missing user')
        if 'user' in kwargs:
            self.u_user = kwargs['user']
            if not self.pk:
                self.c_user = kwargs['user']
            del kwargs['user']
        if 'user_id' in kwargs:
            self.u_user_id = kwargs['user_id']
            if not self.pk:
                self.c_user_id = kwargs['user_id']
            del kwargs['user_id']
        self.u_date = datetime.datetime.now()
        super(base, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if 'user' not in kwargs and 'user_id' not in kwargs:
            raise Exception('missing user for delete')
        self.d_date = datetime.datetime.now()
        if 'user' in kwargs:
            self.d_user = kwargs['user']
        if 'user_id' in kwargs:
            self.d_user_id = kwargs['user_id']
        self.active = False
        self.save()

    class Meta():
        abstract = True

class Server(base):
    url = models.URLField()
    name = models.CharField(max_length=255)
    short = models.CharField(max_length=5)
    version = models.CharField(max_length=5)
    fields = models.TextField(null=True)

    def __unicode__(self):
        return self.name

class boards(base):
    name = models.CharField(max_length=255)
    columns = models.TextField()

    def __unicode__(self):
        return self.name

class tickets_reports(base):
    name = models.CharField(max_length=255)
    search = models.TextField()

    def __unicode__(self):
        return self.name
