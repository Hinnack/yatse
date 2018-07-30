# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django import get_version as get_django_version
from django.utils.translation import ugettext as _
from django.utils.http import urlquote_plus
from yatse.models import tickets_reports
from yatse.forms import SearchForm, AddToBordForm
from yatse.models import boards
from yatse import get_version, get_python_version
from yatse.shortcuts import clean_search_values, add_breadcrumbs, prettyValues
from yatse.api import searchTickets

import datetime

try:
    import json
except ImportError:
    from django.utils import simplejson as json

@login_required
def root(request):
    return render(request, "home.html", {})

@login_required
def info(request):
    from socket import gethostname

    return render(request, "info.html", {'hostname': gethostname(), 'version': get_version(), 'date': datetime.datetime.now(), 'django': get_django_version(), 'python': get_python_version()})

@login_required
def table(request, **kwargs):
    if 'search' in kwargs:
        is_search = True
        params = kwargs['search']
        #raise Exception(params)

    else:
        params = {'closed': False}
        is_search = False

    tic = searchTickets(request, params)
    tic = sorted(tic, key=lambda ticket: ticket['id'])

    pretty = prettyValues(params)
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

@login_required
def show_board(request, name):
    # http://bootsnipp.com/snippets/featured/kanban-board

    """
        board structure

        [
            {
                'column': 'closed',
                'query': {'closed': False},
                'limit': 10,
                'extra_filter': 1, # 1 = days since closed, 2 = days since created, 3 = days since last changed, 4 days since last action
                'days': 1, # days
                'order_by': 'id',
                'order_dir': ''
            }
        ]
    """

    if request.method == 'POST':
        if 'method' in request.POST:
            board = boards.objects.get(active_record=True, pk=request.POST['board'], c_user=request.user)
            try:
                columns = json.loads(board.columns)
            except:
                columns = []

            if request.POST['method'] == 'add':
                form = AddToBordForm(request.POST)
                if form.is_valid():
                    cd = form.cleaned_data
                    col = {
                           'column': cd['column'],
                           'query': request.session['last_search'],
                           'limit': cd['limit'],
                           'order_by': cd['order_by'],
                           'order_dir': cd['order_dir']
                           }
                    if cd.get('extra_filter') and cd.get('days'):
                        col['extra_filter'] = cd['extra_filter']
                        col['days'] = cd['days']
                    columns.append(col)
                    board.columns = json.dumps(columns, cls=DjangoJSONEncoder)
                    board.save(user=request.user)

                else:
                    err_list = []
                    for field in form:
                        for err in field.errors:
                            err_list.append('%s: %s' % (field.name, err))
                    messages.add_message(request, messages.ERROR, _('data invalid: %s') % '\n'.join(err_list))

                return HttpResponseRedirect('/board/%s/' % urlquote_plus(board.name))

        else:
            if request.POST['boardname'].strip() != '':
                if boards.objects.filter(active_record=True, c_user=request.user, name=request.POST['boardname']).count() == 0 and request.POST['boardname']:
                        board = boards()
                        board.name = request.POST['boardname'].strip()
                        board.save(user=request.user)

                        return HttpResponseRedirect('/board/%s/' % urlquote_plus(request.POST['boardname']))

                else:
                    messages.add_message(request, messages.ERROR, _(u'A board with the name "%s" already exists' % request.POST['boardname']))
                    return HttpResponseRedirect('/')
            else:
                messages.add_message(request, messages.ERROR, _(u'No name for a board given'))
                return HttpResponseRedirect('/')

    else:
        board = boards.objects.get(active_record=True, name=name, c_user=request.user)
        try:
            columns = json.loads(board.columns)
        except:
            columns = []

        if 'method' in request.GET and request.GET['method'] == 'del':
            new_columns = []
            for col in columns:
                if col['column'] != request.GET['column']:
                    new_columns.append(col)
            board.columns = json.dumps(new_columns, cls=DjangoJSONEncoder)
            board.save(user=request.user)

            return HttpResponseRedirect('/board/%s/' % urlquote_plus(name))

        elif 'method' in request.GET and request.GET['method'] == 'delete':
            board.delete(user=request.user)
            return HttpResponseRedirect('/')

    for column in columns:
        params = column['query']
        column['query'] = searchTickets(request, params)
        if column['limit']:
            column['query'] = column['query'][:column['limit']]

        if column.get('order_by') == 'close_date':
            for tic in column['query']:
                if 'close_date' not in tic or not tic['close_date']:
                    tic['close_date'] = datetime.datetime(2000, 1, 1)

        column['query'] = sorted(column['query'], key=lambda ticket: ticket[column.get('order_by', 'id')], reverse=column.get('order_dir', '') == '-')

        # todo: days
        """
        column['query'] = query.order_by('%s%s' % (column.get('order_dir', ''), column.get('order_by', 'id')))
        if 'extra_filter' in column and 'days' in column and column['extra_filter'] and column['days']:
            if column['extra_filter'] == '1':  # days since closed
                column['query'] = column['query'].filter(close_date__gte=datetime.date.today() - datetime.timedelta(days=column['days'])).exclude(close_date=None)
            if column['extra_filter'] == '2':  # days since created
                column['query'] = column['query'].filter(c_date__gte=datetime.date.today() - datetime.timedelta(days=column['days']))
            if column['extra_filter'] == '3':  # days since last changed
                column['query'] = column['query'].filter(u_date__gte=datetime.date.today() - datetime.timedelta(days=column['days']))
            if column['extra_filter'] == '4':  # days since last action
                column['query'] = column['query'].filter(last_action_date__gte=datetime.date.today() - datetime.timedelta(days=column['days']))
        """
    add_breadcrumbs(request, board.pk, '$')
    return render(request, 'board/view.html', {'columns': columns, 'board': board})

@login_required
def board_by_id(request, id):
    board = boards.objects.get(active_record=True, pk=id, c_user=request.user)
    return show_board(request, board.name)

@login_required
def reports(request):
    if 'report' in request.GET:
        rep = tickets_reports.objects.get(pk=request.GET['report'])
        add_breadcrumbs(request, request.GET['report'], '@')
        request.session['last_search'] = json.loads(rep.search)
        return HttpResponseRedirect('/tickets/search/?report=%s' % request.GET['report'])

    if 'delReport' in request.GET:
        tickets_reports.objects.filter(c_user=request.user, pk=request.GET['delReport']).delete()
        return HttpResponseRedirect('/reports/')

    reps = tickets_reports.objects.filter(c_user=request.user).order_by('name')

    paginator = Paginator(reps, 10)
    page = request.GET.get('page')
    try:
        rep_lines = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        rep_lines = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        rep_lines = paginator.page(paginator.num_pages)

    return render(request, 'tickets/reports.html', {'lines': rep_lines})
