from django.shortcuts import render, redirect
from user_dictionary.forms import (UserProfileForm, UserDictionaryDetailForm, AddWordInDictForm, AddUserGroupForm,
                                   RegisterForm, LoginForm)
from user_dictionary.service_layer.user_dictionary_access import UserDictionaryAccess
from user_dictionary.service_layer.user_data_access import UserDataAccess
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from user_dictionary.service_layer.pagination_and_search import get_paginator


def main(request):
    return render(request, 'main.html')


@login_required(login_url="register_user")
def dictionary_list(request):
    filters, posts, word_filter = get_paginator(request=request)
    context = {'user_dictionary_list': posts, 'form': word_filter.form, 'filters': filters}
    return render(request, 'user_dictionary/dictionary_list.html', context=context)


@login_required(login_url="register_user")
def group_list(request):
    context = {'user_group_list': UserDictionaryAccess(request).get_user_group_list()}
    return render(request, 'user_dictionary/group_list.html', context=context)


@login_required(login_url="register_user")
def get_user_profile(request):
    user_profile_form = UserProfileForm(request.POST or None,
                                        instance=UserDataAccess(request=request).get_user_account())
    context = {'form': user_profile_form}
    if request.POST and user_profile_form.is_valid():
        user_profile_form.save()
        return redirect("get_user_profile")
    return render(request, 'user_dictionary/profile.html', context=context)


def get_user_word_detail(request, pk):
    user_word_detail = UserDictionaryAccess(request=request).get_user_word_details(pk)
    user_dictionary_details_form = UserDictionaryDetailForm(request.POST or None, instance=user_word_detail)
    user_dictionary_details_form.fields["groups"].queryset = UserDictionaryAccess(request).get_user_group_list()
    context={'form': user_dictionary_details_form, 'user_word': user_word_detail}
    if request.POST and user_dictionary_details_form.is_valid():
        user_dictionary_details_form.save()
        # return redirect(reverse('get_user_word_detail', kwargs={'pk': pk}))
        return redirect("dictionary_list")
    return render(request, 'user_dictionary/word_in_dict_detail.html', context=context)


@login_required(login_url="register_user")
def create_user_word(request):
    if request.method == 'POST':
        add_word_in_dict_form = AddWordInDictForm(request.POST, request=request)

        if add_word_in_dict_form.is_valid():
            add_word_in_dict_form.save()
            return redirect("dictionary_list")
    else:
        add_word_in_dict_form = AddWordInDictForm(request=request,
                                                  initial={'groups': UserDictionaryAccess(request).get_default_group()})
    context = {'form': add_word_in_dict_form}
    print(add_word_in_dict_form.errors)
    return render(request, 'user_dictionary/add_word_in_dict.html', context=context)


@login_required(login_url="register_user")
def create_user_group(request):
    if request.method == 'POST':
        add_user_group_form = AddUserGroupForm(request.POST, request=request)
        if add_user_group_form.is_valid():
            add_user_group_form.save()
            return redirect('group_list')
    else:
        add_user_group_form = AddUserGroupForm(request=request)
    context = {'form': add_user_group_form}
    return render(request, 'user_dictionary/add_user_group.html', context=context)


class RegisterUser(FormView):
    form_class = RegisterForm
    template_name = 'register_form.html'
    success_url = reverse_lazy('dictionary_list')

    def form_valid(self, form):
        new_user = form.save()
        login(self.request, new_user)
        return super(RegisterUser, self).form_valid(form)


class LoginUser(LoginView):
    authentication_form = LoginForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('dictionary_list')


def delete_user_group(request, pk):
    UserDictionaryAccess(request).delete_user_group(pk=pk)
    return redirect('group_list')


def delete_user_word(request, pk):
    UserDictionaryAccess(request).delete_user_word(pk=pk)
    return redirect('dictionary_list')


