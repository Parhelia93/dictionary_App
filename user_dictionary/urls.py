from django.urls import path
from dictionary_App import settings
from django.contrib.auth.views import LogoutView
from user_dictionary.views import (dictionary_list, group_list,
                                   get_user_profile, get_user_word_detail, create_user_word, create_user_group, RegisterUser, LoginUser, main, delete_user_group, delete_user_word)
urlpatterns = [
    path('dictionary_list/', dictionary_list, name='dictionary_list'),
    path('group_list/', group_list, name='group_list'),
    path('profile/', get_user_profile, name='get_user_profile'),
    path('user_word/<int:pk>', get_user_word_detail, name='get_user_word_detail'),
    path('add_word_in_dict/', create_user_word, name='create_user_word'),
    path('add_user_group/', create_user_group, name='create_user_group'),
    path('register/', RegisterUser.as_view(), name='register_user'),
    path('login/', LoginUser.as_view(), name='login'),
    path('main/', main, name='main'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('delete_user_group/<int:pk>', delete_user_group, name='delete_user_group'),
    path('delete_user_word/<int:pk>', delete_user_word, name='delete_user_word'),
]
