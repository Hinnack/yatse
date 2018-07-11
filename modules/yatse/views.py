# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.conf import settings
from yatse.models import tickets_reports
from yatse.forms import SearchForm

def root(request):
    return render(request, "home.html", {})

def info(request):
    return render(request, "info.html", {})

def table(request, **kwargs):
    search_params = {}
    mod_path, cls_name = settings.TICKET_CLASS.rsplit('.', 1)
    mod_path = mod_path.split('.').pop(0)
    tic = get_model(mod_path, cls_name).objects.select_related('type').all()

    if not request.user.is_staff:
        tic = tic.filter(customer=request.organisation)

    if 'search' in kwargs:
        is_search = True
        params = kwargs['search']

        if not request.user.is_staff:
            used_fields = []
            for ele in settings.TICKET_SEARCH_FIELDS:
                if not ele in settings.TICKET_NON_PUBLIC_FIELDS:
                    used_fields.append(ele)
        else:
            used_fields = settings.TICKET_SEARCH_FIELDS

        Qr = None
        fulltext = {}
        for field in params:
            if field == 'fulltext':
                if field in used_fields and get_ticket_model()._meta.get_field(field).get_internal_type() == 'CharField':
                    fulltext['%s__icontains' % field] = params[field]

            else:
                if params[field] != None and params[field] != '':
                    if get_ticket_model()._meta.get_field(field).get_internal_type() == 'CharField':
                        search_params['%s__icontains' % field] = params[field]
                    else:
                        search_params[field] = params[field]

        tic = tic.filter(**search_params)
    else:
        tic = tic.filter(closed=False)
        is_search = False

    pretty = prettyValues(search_params)
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
    board_form.fields['board'].queryset = board_form.fields['board'].queryset.filter(c_user=request.user)

    return render_to_response('tickets/list.html', {'lines': tic_lines, 'is_search': is_search, 'pretty': pretty, 'list_caption': list_caption, 'board_form': board_form}, RequestContext(request))

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
        form = SearchForm(request.POST, include_list=searchable_fields, is_stuff=request.user.is_staff, user=request.user, customer=request.organisation.id)
        form.is_valid()
        request.session['last_search'] = clean_search_values(form.cleaned_data)
        request.session['last_search_caption'] = ''

        return table(request, search=request.session['last_search'])

    if 'last_search' in request.session and 'new' not in request.GET:
        return table(request, search=request.session['last_search'], list_caption=request.session.get('last_search_caption', ''))

    form = SearchForm(include_list=searchable_fields, is_stuff=request.user.is_staff)

    return render(request, "tickets/search.html", {'layout': 'horizontal', 'form': form})
