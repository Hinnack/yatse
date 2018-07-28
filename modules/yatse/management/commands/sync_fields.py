# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User
from yatse.models import Server
import requests

class Command(BaseCommand):
    args = '<>'
    help = 'sync fields from yats server'

    def handle(self, *args, **options):
        api_user = User.objects.filter(is_active=True, is_superuser=True)[0]

        headers = {
            'user-agent': 'yatse/0.0.1',
            'api-key': settings.API_KEY,
            'api-user': api_user.username
        }

        for Srv in Server.objects.all():
            self.stdout.write('syncing fields of %s\n' % Srv.url)
            url = '%s/yatse/' % Srv.url
            req = requests.request('PROPFIND', url, headers=headers)
            if req.status_code == 200:
                Srv.fields = req.text
                Srv.save(user=api_user)
                self.stdout.write('OK')

            else:
                self.stdout.write('error %s\n' % req.status_code)

        self.stdout.write('done')
