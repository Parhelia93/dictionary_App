from django.db.models.signals import post_save
from user_dictionary.models import UserAccount, GroupOfUserWord, Word
from django.contrib.auth.models import User
from user_dictionary.utils import check_available_file_in_folder
from user_dictionary.tasks import create_audio_file_worker
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File


def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = UserAccount.objects.create(
            django_user=user
        )


def create_default_user_group(sender, instance, created, **kwargs):
    if created:
        user_profile = instance
        default_user_group = GroupOfUserWord.objects.create(
            name='Default',
            account=user_profile
        )


def link_word_with_audio(sender, instance, created, **kwargs):
    if created:
        word = instance
        if check_available_file_in_folder(f'{word.word}.mp3'):
            with NamedTemporaryFile() as f:
                word.audio.save(f'{word.word}.mp3', File(f, 'rb'))
                word.save()
        else:
            create_audio_file_worker.apply_async(args=[word.word], countdown=10)


# def delete_user_audiofile(sender, instance, **kwargs):
#     if check_available_file_in_folder(f'{instance.word}.mp3'):
#         print('deleting file...')
#         remove_media_file(f'{instance.word}.mp3')


post_save.connect(create_profile, sender=User)
post_save.connect(create_default_user_group, sender=UserAccount)
post_save.connect(link_word_with_audio, sender=Word)
# post_delete.connect(delete_user_audiofile, sender=Word)
