import django_filters
from user_dictionary.models import UserDictionary
from django_filters.widgets import BooleanWidget
from django import forms
from django.db import models


class CustomBooleanWidget(BooleanWidget):
    def __init__(self, attrs=None, choices=()):
        # remove the 'unknown' option here
        choices = (('', "---------"),('true', 'Yes'), ('false', 'No'))

        # bypass BooleanWidget.__init__
        forms.Select.__init__(self, attrs, choices)


class WordFilter(django_filters.FilterSet):
    user_word__word = django_filters.CharFilter(lookup_expr='icontains', label='Word')

    class Meta:
        model = UserDictionary
        fields = ['user_word__word', 'translate', 'part_of_speach', 'status_of_learn']
        filter_overrides = {
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': CustomBooleanWidget,
                },
            }
        }

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super(WordFilter, self).__init__(data=data, queryset=queryset, request=request, prefix=prefix)
        self.filters['user_word__word'].field.widget.attrs.update({'class': 'uk-input uk-form-small'})
        self.filters['translate'].field.widget.attrs.update({'class': 'uk-input uk-form-small'})
        self.filters['part_of_speach'].field.widget.attrs.update({'class': 'uk-select uk-form-small'})
        self.filters['status_of_learn'].field.widget.attrs.update({'class': 'uk-select uk-form-small'})

        
