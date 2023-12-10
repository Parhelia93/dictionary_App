from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import reverse


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class UserAccount(BaseModel):
    django_user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_id = models.IntegerField(default=0)
    user_dictionary_words = models.ManyToManyField('Word', through='UserDictionary')
    num_of_days_until_reset_status_learned = models.IntegerField(default=30)
    notifications_enable = models.BooleanField(default=True)
    length_of_training = models.IntegerField(default=5)

    def __str__(self):
        return self.django_user.username


class Word(models.Model):
    word = models.CharField(max_length=30, unique=True)
    audio = models.FileField(blank=True, upload_to='words')
    telegram_file_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.word

    def save(self, *args, **kwargs):
        self.word = self.word.lower()
        super(Word, self).save(*args, **kwargs)


class UserDictionary(BaseModel):
    CHOICES = (
        ('verb', 'verb'),
        ('noun', 'noun'),
        ('adjective', 'adjective'),
        ('numerals', 'numerals'),
        ('adverb', 'adverb'),
    )

    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    user_word = models.ForeignKey(Word, on_delete=models.CASCADE)
    translate = models.CharField(max_length=30)
    usage_example = models.TextField(max_length=200)
    part_of_speach = models.CharField(max_length=20, choices=CHOICES)
    status_of_learn = models.BooleanField(default=False)
    groups = models.ManyToManyField('GroupOfUserWord')
    __original_status = None

    def __str__(self):
        return f'{self.user_account}:{self.user_word}'

    def delete_user_word_url(self):
        return reverse('delete_user_word', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return reverse('get_user_word_detail', kwargs={'pk': self.pk})

    def __init__(self, *args, **kwargs):
        super(UserDictionary, self).__init__(*args, **kwargs)
        self.__original_status = self.status_of_learn

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.translate = self.translate.lower()
        if self.status_of_learn != self.__original_status:
            HistoryOfLearnedWord.objects.create(user_dictionary=self, learned_status=self.status_of_learn)
        super(UserDictionary, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_status = self.status_of_learn


class StatisticOfWordInDictionary(models.Model):
    user_dictionary = models.ForeignKey(UserDictionary, on_delete=models.CASCADE)
    user_answer = models.BooleanField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user_dictionary}:{self.user_answer}'


class GroupOfUserWord(BaseModel):
    name = models.CharField(max_length=20)
    account = models.ForeignKey('UserAccount', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    def delete_user_group_url(self):
        return reverse('delete_user_group', kwargs={'pk': self.pk})


class HistoryOfLearnedWord(BaseModel):
    user_dictionary = models.ForeignKey(UserDictionary, on_delete=models.CASCADE)
    learned_status = models.BooleanField()
