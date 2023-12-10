from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from user_dictionary.models import UserAccount
from user_dictionary.service_layer import data_fetch_helper


class UserDataAccess:
    """
    WORK WITH USER DATA
    1. Get UserAccount from SQL
    """
    def __init__(self, request: HttpRequest):
        self.user = self.__get_user_from_request(request=request)

    @staticmethod
    def __get_user_from_request(request: HttpRequest) -> User | None:
        user_from_request = get_user(request)
        if user_from_request.is_authenticated:
            return user_from_request
        else:
            return None

    def get_user_account(self) -> UserAccount | None:
        return data_fetch_helper.get_or_none(UserAccount, django_user=self.user)
