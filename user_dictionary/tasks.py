from gtts import gTTS
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from celery import shared_task
from user_dictionary.service_layer.word_data_access import WordDataAccess


@shared_task
def create_audio_file_worker(input_word):
    word = WordDataAccess.get_word(input_word)
    with NamedTemporaryFile() as f:
        audio = gTTS(str(word))
        for chunk in audio.stream():
            f.write(chunk)
        word.audio.save(f'{word.word}.mp3', File(f, 'rb'))
        word.save()

