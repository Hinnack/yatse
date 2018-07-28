# -*- coding: utf-8 -*-
import datetime

def clean_search_values(search):
    result = {}
    for ele in search:
        if type(search[ele]) not in [bool, int, str, unicode, long, None, datetime.date]:
            if search[ele]:
                result[ele] = search[ele].pk
        else:
            result[ele] = search[ele]
    return result

def add_breadcrumbs(request, pk, typ):
    breadcrumbs = request.session.get('breadcrumbs', [])
    # checks if already exists
    if len(breadcrumbs) > 0:
        if breadcrumbs[-1][0] != long(pk) or breadcrumbs[-1][1] != typ:
            if (long(pk), typ,) in breadcrumbs:
                breadcrumbs.pop(breadcrumbs.index((long(pk), typ,)))
            breadcrumbs.append((long(pk), typ,))

    else:
        breadcrumbs.append((long(pk), typ,))
    while len(breadcrumbs) > 10:
        breadcrumbs.pop(0)
    request.session['breadcrumbs'] = breadcrumbs
