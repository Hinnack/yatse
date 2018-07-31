# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.utils.timezone import is_naive, make_aware
from yatse.models import Server
from requests_futures.sessions import FuturesSession
import dateutil.parser
import datetime

try:
    import json
except ImportError:
    from django.utils import simplejson as json

def searchTickets(request, params):
    session = FuturesSession()
    async_list = []
    tic = []
    headers = {
        'user-agent': 'yatse/0.0.1',
        'api-key': settings.API_KEY,
        'api-user': request.user.username
    }
    for Srv in Server.objects.all():
        url = '%s/yatse/' % Srv.url
        # , hooks={'response': do_something}
        req = session.request('SEARCH', url, data=json.dumps(params), headers=headers)
        setattr(req, 'serverName', Srv.name)
        setattr(req, 'serverID', Srv.id)
        setattr(req, 'serverShortName', Srv.short)
        async_list.append(req)

    for req in async_list:
        try:
            result = req.result()
            if result.status_code != 200:
                messages.add_message(request, messages.ERROR, _(u'%s respoded width: %s' % (req.serverName, result.status_code)))

            else:
                data = json.loads(result.content)
                for date in data:
                    date['YATSServer'] = req.serverShortName
                    date['serverID'] = req.serverID
                    date['c_date'] = dateutil.parser.parse(date['c_date'])
                    date['last_action_date'] = dateutil.parser.parse(date['last_action_date'])
                    if is_naive(date['last_action_date']):
                        date['last_action_date'] = make_aware(date['last_action_date'])
                    if 'close_date' in date and date['close_date']:
                        date['close_date'] = dateutil.parser.parse(date['close_date'])
                    date['is_late'] = 0
                    if 'daedline' in date and date['daedline']:
                        date['daedline'] = dateutil.parser.parse(date['daedline'])
                        if date['daedline'] < datetime.date.today():
                            date['is_late'] = 2
                        if date['daedline'] < datetime.date.today() + datetime.timedelta(days=7):
                            date['is_late'] = 1

                tic = tic + data

        except:
            messages.add_message(request, messages.ERROR, _(u'YATS nicht erreichbar: %s' % req.serverName))

    return tic
