import os
from dictionary_App.settings import MEDIA_ROOT


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


def check_available_file_in_folder(new_word_media_file):
    with os.scandir(MEDIA_ROOT+'/'+'words') as files:
        return True if any([file.name == new_word_media_file for file in files]) else False


def remove_media_file(new_word_media_file):
    os.remove(path=MEDIA_ROOT + '/' + 'words' + '/' + new_word_media_file)
