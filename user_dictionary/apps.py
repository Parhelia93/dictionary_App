from django.apps import AppConfig


class UserDictionaryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_dictionary'

    def ready(self):
        import user_dictionary.signals
