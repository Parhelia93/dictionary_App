from rest_framework.response import Response
from rest_framework.decorators import api_view
from user_dictionary.models import UserAccount, UserDictionary, StatisticOfWordInDictionary, Word
from api.serializers import UserDictionarySerializer
import random


@api_view(['GET'])
def get_routes(request):
    routes = [
        {"GET": "/api/user_dictionaries/telegram_id"},
    ]
    return Response(routes)


@api_view(['GET'])
def get_user_dictionaries(request, telegram_id):
    user_account = UserAccount.objects.get(telegram_id=telegram_id)
    user_dictionaries = UserDictionary.objects.filter(user_account=user_account, status_of_learn=False)
    list_of_word = list()
    for _ in range(user_account.length_of_training):
        list_of_word.append(random.choice(user_dictionaries))
    serializer = UserDictionarySerializer(list_of_word, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def user_answer(request, pk):
    user_dictionary = UserDictionary.objects.get(pk=pk)
    user_reply = request.data['answer']
    statistic = StatisticOfWordInDictionary(user_dictionary=user_dictionary, user_answer=user_reply)
    statistic.save()
    return Response()


@api_view(['GET'])
def verify_user(request, telegram_id):
    #Hard code, need to fix
    user_acc = UserAccount.objects.filter(telegram_id=telegram_id).count()
    if user_acc == 1:
        return Response({"verify": "True"})
    else:
        return Response({"verify": "False"})


@api_view(['PUT'])
def update_word_telegram_file_id(request, pk):
    # Hard code, need to fix
    file_id = request.data['file_id']
    word = Word.objects.get(pk=pk)
    word.telegram_file_id = file_id
    word.save()
    return Response()
