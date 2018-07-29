# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from bootstrap_toolkit.widgets import BootstrapDateInput
from yatse.models import Server, boards
from yatse.shortcuts import fieldNameToTracName
import datetime
import json

ORDER_BY_CHOICES = (
    ('id', _('ticket number')),
    ('close_date', _('closing date')),
    ('last_action_date', _('last changed'))
)

ORDER_DIR_CHOICES = (
    ('', _('ascending')),
    ('-', _('descending'))
)

POST_FILTER_CHOICES = (
    (0, '-------------'),
    (1, _('days since closed')),
    (2, _('days since created')),
    (3, _('days since last changed')),
    (4, _('days since last action')),
)

class AddToBordForm(forms.Form):
    method = forms.CharField(widget=forms.HiddenInput(), initial='add')
    board = forms.ModelChoiceField(queryset=boards.objects.filter(active_record=True), label=_('board'), empty_label=None)
    column = forms.CharField(label=_('column'))
    limit = forms.IntegerField(label=_('limit'), required=False)
    extra_filter = forms.ChoiceField(choices=POST_FILTER_CHOICES, label=_('extra filter'), required=False)
    days = forms.IntegerField(label=_('days'), required=False)
    order_by = forms.ChoiceField(choices=ORDER_BY_CHOICES, label=_('order by'))
    order_dir = forms.ChoiceField(choices=ORDER_DIR_CHOICES, label=_('order direction'), required=False)

class dynamicForm(forms.Form):
    """
    dynamic fields form
    """

    def __init__(self, *args, **kwargs):
        self.select_vars = []
        super(dynamicForm, self).__init__(*args, **kwargs)

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
            field = forms.ChoiceField(widget=forms.Select(attrs={'style': 'font-family: \'FontAwesome\', \'sans-serif\';'}), choices=options, label=label, required=False)
            self.select_vars.append(varname)

        if fieldtype == 11:  # dateshort
            initial = self.getDefaultDate(initial)
            field = forms.DateField(label=label, required=False)

        if field:
            setattr(self, varname, field)
            self.fields[varname] = field
        else:
            raise Exception('missing field type %s' % fieldtype)

    def clean(self):
        cleaned_data = super(dynamicForm, self).clean()

        for ele in self.select_vars:
            if ele in cleaned_data and not cleaned_data[ele]:
                del cleaned_data[ele]
        return cleaned_data


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
            foundAllOptions = True
            type = None
            options = []

            for server in Server.objects.all():
                found = False
                fields = json.loads(server.fields)
                for field in fields:
                    if fieldname in field['name']:
                        found = True
                        type = field['type']
                        options = options + field.get('options', [])
                        label = fieldNameToTracName(fieldname)
                        break
                if not found:
                    foundInAll = False

            if not foundInAll:
                op = [(opt, '%s &#xf0b0;' % opt) for opt in list(set(options))]
            else:
                op = [(opt, opt) for opt in list(set(options))]
            if len(op):
                op.insert(0, ('', '---------'))

            self.addField(type, fieldname, label, op)
