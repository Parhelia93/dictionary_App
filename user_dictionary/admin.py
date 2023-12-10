from django.contrib import admin
from user_dictionary.models import (UserAccount, Word, UserDictionary,
                                    StatisticOfWordInDictionary, GroupOfUserWord, HistoryOfLearnedWord)

admin.site.register(UserAccount)
admin.site.register(Word)
admin.site.register(UserDictionary)
admin.site.register(StatisticOfWordInDictionary)
admin.site.register(GroupOfUserWord)
admin.site.register(HistoryOfLearnedWord)
