# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django import get_version as get_django_version
from django.utils.translation import ugettext as _
from yatse.models import tickets_reports
from yatse.forms import SearchForm, AddToBordForm
from yatse.models import Server
from yatse import get_version, get_python_version
from yatse.shortcuts import clean_search_values

from requests_futures.sessions import FuturesSession
import datetime

@login_required
def root(request):
    return render(request, "home.html", {})

@login_required
def info(request):
    from socket import gethostname

    return render(request, "info.html", {'hostname': gethostname(), 'version': get_version(), 'date': datetime.datetime.now(), 'django': get_django_version(), 'python': get_python_version()})

@login_required
def table(request, **kwargs):
    search_params = {}
    tic = []

    if 'search' in kwargs:
        is_search = True
        params = kwargs['search']

    else:
        params = {'closed': False}
        is_search = False

    session = FuturesSession()
    async_list = []
    for Srv in Server.objects.all():
        url = '%yatsee/?%s' % (Srv.url)
        # , hooks={'response': do_something}
        req = session.search(url)
        setattr(req, 'serverName', Srv.name)
        async_list.append(req)
    for req in async_list:
        result = req.result()
        try:
            # aaa = 'response status: {0}'.format(result.status_code)
            if result.status_code != 200:
                messages.add_message(request, messages.ERROR, _(u'%s respoded width: %s' % (req.serverName, result.status_code)))

        except:
            # req._exception.request.url
            messages.add_message(request, messages.ERROR, _(u'YATS nicht erreichbar: %s' % req.serverName))

    pretty = search_params
    list_caption = kwargs.get('list_caption')
    if 'report' in request.GET:
        list_caption = tickets_reports.objects.get(pk=request.GET['report']).name

    paginator = Paginator(tic, 20)
    page = request.GET.get('page')
    try:
        tic_lines = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tic_lines = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tic_lines = paginator.page(paginator.num_pages)

    board_form = AddToBordForm()
    #board_form.fields['board'].queryset = board_form.fields['board'].queryset.filter(c_user=request.user)

    return render(request, 'tickets/list.html', {'lines': tic_lines, 'is_search': is_search, 'pretty': pretty, 'list_caption': list_caption, 'board_form': board_form})

@login_required
def search(request):
    searchable_fields = settings.TICKET_SEARCH_FIELDS

    if request.method == 'POST' and 'reportname' in request.POST and request.POST['reportname']:
        rep = tickets_reports()
        rep.name = request.POST['reportname']
        rep.search = json.dumps(request.session['last_search'], cls=DjangoJSONEncoder)
        rep.save(user=request.user)

        request.session['last_search'] = clean_search_values(request.session['last_search'])
        request.session['last_search_caption'] = request.POST['reportname']

        return table(request, search=request.session['last_search'], list_caption=request.session['last_search_caption'])

    if request.method == 'POST':
        form = SearchForm(request.POST, include_list=searchable_fields, is_stuff=request.user.is_staff)
        form.is_valid()
        request.session['last_search'] = clean_search_values(form.cleaned_data)
        request.session['last_search_caption'] = ''

        return table(request, search=request.session['last_search'])

    if 'last_search' in request.session and 'new' not in request.GET:
        return table(request, search=request.session['last_search'], list_caption=request.session.get('last_search_caption', ''))

    form = SearchForm(include_list=searchable_fields, is_stuff=request.user.is_staff)

    return render(request, "tickets/search.html", {'layout': 'horizontal', 'form': form})
