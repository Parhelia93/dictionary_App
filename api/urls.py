from django.urls import path
from api import views

urlpatterns = [
    path('', views.get_routes),
    path('user_dictionaries/<int:telegram_id>', views.get_user_dictionaries),
    path('user_reply/<int:pk>', views.user_answer),
    path('verify_user/<int:telegram_id>', views.verify_user),
    path('update_file_id/<int:pk>', views.update_word_telegram_file_id)
]
