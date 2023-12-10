from django import forms
from user_dictionary.models import UserAccount, UserDictionary, Word, GroupOfUserWord
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from user_dictionary.service_layer.validation_user_input import check_input_word
from collections import defaultdict
from user_dictionary.service_layer.user_dictionary_access import UserDictionaryAccess
from user_dictionary.service_layer.data_fetch_helper import get_or_none
from user_dictionary.service_layer.user_data_access import UserDataAccess


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['telegram_id', 'num_of_days_until_reset_status_learned', 'length_of_training', 'notifications_enable']
        widgets = {
            'telegram_id': forms.TextInput(attrs={'class': 'uk-input'}),
            'num_of_days_until_reset_status_learned': forms.TextInput(attrs={'class': 'uk-input'}),
            'notifications_enable': forms.CheckboxInput(attrs={'class': 'uk-checkbox'}),
            'length_of_training': forms.TextInput(attrs={'class': 'uk-input'}),
        }


class UserDictionaryDetailForm(forms.ModelForm):
    class Meta:
        model = UserDictionary
        fields = ['translate', 'usage_example', 'part_of_speach', 'status_of_learn', 'groups']
        widgets = {
            'translate': forms.TextInput(attrs={'class': 'uk-input'}),
            'usage_example': forms.Textarea(attrs={'class': 'uk-textarea'}),
            'part_of_speach': forms.Select(attrs={'class': 'uk-select'}),
            'status_of_learn': forms.CheckboxInput(attrs={'class': 'uk-checkbox'}),
            'groups': forms.CheckboxSelectMultiple()
        }


class AddWordInDictForm(forms.ModelForm):
    word = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'uk-input'}))

    class Meta:
        model = UserDictionary
        fields = ['word', 'translate', 'usage_example', 'part_of_speach', 'groups']
        widgets = {
            'translate': forms.TextInput(attrs={'class': 'uk-input'}),
            'usage_example': forms.Textarea(attrs={'class': 'uk-textarea'}),
            'part_of_speach': forms.Select(attrs={'class': 'uk-select'}),
            'groups': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AddWordInDictForm, self).__init__(*args, **kwargs)
        self.fields['part_of_speach'].empty_label = None
        if self.request:
            self.fields['groups'].choices = \
                [(choice.pk, choice) for choice in UserDictionaryAccess(self.request).get_user_group_list()]

    def save(self, commit=True):
        instance = super(AddWordInDictForm, self).save(commit=False)
        word, created = Word.objects.get_or_create(word=self.cleaned_data['word'])
        instance.user_word = word

        user = UserDataAccess(self.request).get_user_account()
        self.cleaned_data.pop('word', None)
        instance.user_account = user
        if commit:
            instance.save()
            self.save_m2m()
        return instance

    def clean(self):
        error = defaultdict(lambda: "Not Present")
        cleaned_data = super().clean()
        user_account = UserDataAccess(self.request).get_user_account()
        word = get_or_none(Word, word=cleaned_data['word'])
        if get_or_none(UserDictionary, user_word=word, translate=cleaned_data['translate'], user_account=user_account):
            self.add_error(field=None, error='Word is already exist')

        if check_input_word(cleaned_data['word']):
            self.add_error(field=None, error='Word error')

        return cleaned_data


class AddUserGroupForm(forms.ModelForm):
    class Meta:
        model = GroupOfUserWord
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'uk-input'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AddUserGroupForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(AddUserGroupForm, self).save(commit=False)
        user = UserDataAccess(self.request).get_user_account()
        instance.account = user
        instance.save()
        return instance

    def clean(self):
        cleaned_data = super().clean()
        user_account = UserDataAccess(self.request).get_user_account()
        if get_or_none(GroupOfUserWord, name=cleaned_data['name'], account=user_account):
            raise forms.ValidationError('Already exist')
        return cleaned_data


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
