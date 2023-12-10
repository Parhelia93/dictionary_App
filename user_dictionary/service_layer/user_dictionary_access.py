from django.http import HttpRequest
from user_dictionary.models import UserDictionary, GroupOfUserWord
from typing import Iterable
from user_dictionary.service_layer.user_data_access import UserDataAccess
from user_dictionary.service_layer import data_fetch_helper


class UserDictionaryAccess:
    """
    WORK WITH USER DATA FROM SQL:
    1. Get User Dictionary List
    2. Get User Group List
    3. Get User Word Detail
    4. Delete User Word
    5. Delete User Group
    6. Get Default group
    """

    def __init__(self, request: HttpRequest):
        self.user = UserDataAccess(request=request).get_user_account()

    def get_user_dictionary_list(self) -> Iterable[UserDictionary]:
        return data_fetch_helper.get_list_or_none(UserDictionary,
                                                  user_account=self.user)

    def get_user_group_list(self) -> Iterable[GroupOfUserWord]:
        return data_fetch_helper.get_list_or_none(GroupOfUserWord,
                                                  account=self.user)

    def get_default_group(self) -> GroupOfUserWord:
        return data_fetch_helper.get_or_none(GroupOfUserWord, name='Default', account=self.user)

    def get_user_word_details(self, pk: int) -> UserDictionary:
        return data_fetch_helper.get_or_none(UserDictionary, user_account=self.user, pk=pk)

    def delete_user_group(self, pk: int) -> None:
        data_fetch_helper.get_or_none(GroupOfUserWord, pk=pk, account=self.user).delete()

    def delete_user_word(self, pk: int) -> None:
        data_fetch_helper.get_or_none(UserDictionary, user_account=self.user, pk=pk).delete()
