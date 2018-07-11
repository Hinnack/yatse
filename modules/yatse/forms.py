# -*- coding: utf-8 -*-
from django import forms
from bootstrap_toolkit.widgets import BootstrapDateInput
from yatse.models import Server
import datetime
import json

class dynamicForm(forms.Form):
    """
    dynamic fields form
    """

    def getDefaultDate(self, default):
        if default == 'today':
            return datetime.date.today()
        elif default == 'now':
            return datetime.datetime.now()
        elif default == 'tomorrow':
            return datetime.date.today() + datetime.timedelta(days=1)

    def addField(self, fieldtype, varname, label, options, **kwargs):
        field = None
        if fieldtype == 'FloatField':  # float
            field = forms.FloatField(label=label, required=False)

        if fieldtype == 'AutoField':  # int
            field = forms.IntegerField(label=label, required=False)

        if fieldtype == 'BooleanField':  # boolean
            field = forms.NullBooleanField(label=label, required=False)

        if fieldtype == 'NullBooleanField':
            field = forms.NullBooleanField(label=label, required=False)

        if fieldtype == 'CharField' and not options:  # str
            field = forms.CharField(label=label, required=False)

        if fieldtype == 'TextField':  # str
            field = forms.TextField(label=label, required=False)

        if fieldtype == 'DateField':  # date
            field = forms.DateField(widget=BootstrapDateInput(), label=label, required=False)

        if fieldtype == 'TimeField':  # time
            field = forms.TimeField(widget=TimeWidget(), label=label, required=False)

        if fieldtype == 'DateTimeField':  # datetime
            field = forms.DateTimeField(widget=DateTimeWidget(), label=label, required=False)

        if fieldtype == 8:  # enum
            pass

        if fieldtype == 9:  # hidden
            field = forms.CharField(widget=forms.HiddenInput(), label=label, required=False)

        if fieldtype == 'select':  # select
            field = forms.ChoiceField(choices=options, label=label, required=False)

        if fieldtype == 11:  # dateshort
            initial = self.getDefaultDate(initial)
            field = forms.DateField(label=label, required=False)

        if field:
            setattr(self, varname, field)
            self.fields[varname] = field
        else:
            raise Exception('missing field type %s' % fieldtype)

class SearchForm(dynamicForm):
    def __init__(self, *args, **kwargs):
        if 'include_list' in kwargs:
            self.include_list = kwargs['include_list']
            del kwargs['include_list']

        if 'is_stuff' in kwargs:
            self.is_stuff = kwargs['is_stuff']
            del kwargs['is_stuff']

        if 'customer' in kwargs:
            self.customer = kwargs['customer']
            del kwargs['customer']

        super(SearchForm, self).__init__(*args, **kwargs)

        self.init()

    def init(self):
        for fieldname in self.include_list:
            foundInAll = True
            type = None

            for server in Server.objects.all():
                found = False
                fields = json.loads(server.fields)
                for field in fields:
                    if fieldname in field['name']:
                        found = True
                        type = field['type']
                        options = field.get('options', [])
                        label = field['label']
                        break
                if not found:
                    foundInAll = False

            op = [(opt, opt) for opt in options]
            if len(op):
                op.insert(0, ('aa', '------------'))

            self.addField(type, fieldname, label, op)
