from user_dictionary.models import Word
from user_dictionary.service_layer import data_fetch_helper


class WordDataAccess:
    """
    WORK WITH WORD DATA FROM SQL:
    1. Get Word From SQL
    2. Create Word In SQL
    """
    @classmethod
    def get_word(cls, word: str) -> Word | None:
        return data_fetch_helper.get_or_none(Word, word=word)

    @classmethod
    def create_word(cls, word: str) -> None:
        pass
