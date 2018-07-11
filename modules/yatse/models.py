# -*- coding: utf-8 -*-
from django.db import models

class Server(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=255)
    short = models.CharField(max_length=5)
    version = models.CharField(max_length=5)
    fields = models.TextField(null=True)
