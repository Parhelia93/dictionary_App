from rest_framework import serializers
from user_dictionary.models import UserDictionary, Word, GroupOfUserWord


class UserWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['pk', 'word', 'telegram_file_id']


class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupOfUserWord
        fields = ['name']


class UserDictionarySerializer(serializers.ModelSerializer):
    user_word = UserWordSerializer(many=False)
    # groups = GroupsSerializer(many=True)
    
    class Meta:
        model = UserDictionary
        fields = ['pk', 'user_word', 'translate', 'usage_example', 'part_of_speach']
