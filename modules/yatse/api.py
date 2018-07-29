# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext as _
from yatse.models import Server
from requests_futures.sessions import FuturesSession
import dateutil.parser

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
        setattr(req, 'serverURL', Srv.url)
        setattr(req, 'serverShortName', Srv.short)
        async_list.append(req)

    for req in async_list:
        result = req.result()
        try:
            if result.status_code != 200:
                messages.add_message(request, messages.ERROR, _(u'%s respoded width: %s' % (req.serverName, result.status_code)))

            else:
                data = json.loads(result.content)
                for date in data:
                    date['YATSServer'] = req.serverShortName
                    date['YATSServerURL'] = req.serverURL
                    date['c_date'] = dateutil.parser.parse(date['c_date'])
                    # date['daedline'] = dateutil.parser.parse(date['daedline']) if date['daedline'] else None
                    date['is_late'] = 0
                tic = tic + data

        except:
            messages.add_message(request, messages.ERROR, _(u'YATS nicht erreichbar: %s' % req.serverName))

    return tic
