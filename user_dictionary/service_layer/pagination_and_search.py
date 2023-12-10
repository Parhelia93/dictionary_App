from user_dictionary.filters import WordFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpRequest
from user_dictionary.service_layer.user_dictionary_access import UserDictionaryAccess


def get_paginator(request: HttpRequest):
    filters = {
        "user_word__word": request.GET.get("user_word__word", ""),
        "translate": request.GET.get("translate", ""),
        "part_of_speach": request.GET.get("part_of_speach", ""),
        "status_of_learn": request.GET.get("status_of_learn", "")
    }

    word_filter = WordFilter(request.GET, queryset=UserDictionaryAccess(request).get_user_dictionary_list())
    page = request.GET.get('page', 1)
    paginator = Paginator(word_filter.qs, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return filters, posts, word_filter
