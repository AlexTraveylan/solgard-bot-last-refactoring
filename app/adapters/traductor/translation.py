import json
from typing import Literal


class Translate:
    """
    A class that provides functionality to translate between different languages. The currently supported languages
    include French, English, Italian, Spanish, Chinese, and Russian.

    Parameters
    ----------
    lang : Literal["fr", "en", "it", "es", "zh", "ru", "de"]
        The language to be used for translation.

    Attributes
    ----------
    lang : Literal["fr", "en", "it", "es", "zh", "ru", "de"]
        The language to be used for translation.
    translations : dict[str, str]
        A dictionary that maps a word from one language to another.
    """

    def __init__(self, lang: Literal["fr", "en", "it", "es", "zh", "ru", "de"]) -> None:
        self.lang = lang
        self.translations = self.load_translation(lang)

    def load_translation(self, lang: Literal["fr", "en", "it", "es", "zh", "ru", "de"]) -> dict[str, str]:
        """
        Load translations from a specified language file.

        Parameters
        ----------
        lang : Literal["fr", "en", "it", "es", "zh", "ru", "de"]
            The language of the file to load.

        Returns
        -------
        dict[str, str]
            A dictionary containing the translations.

        Raises
        ------
        ValueError
            If the language file was not found or could not be decoded.
        """
        try:
            with open(f"app/adapters/traductor/{lang}.json", encoding="utf-8") as lang_file:
                translations = json.load(lang_file)
                return translations
        except FileNotFoundError:
            raise ValueError(f"Failed to find {lang}.json")
        except json.JSONDecodeError:
            raise ValueError(f"Failed to decode {lang}.json")

    def set_translation(self, lang: Literal["fr", "en", "it", "es", "zh", "ru", "de"]):
        """
        Set the translations to a different language.

        Parameters
        ----------
        lang : Literal["fr", "en", "it", "es", "zh", "ru", "de"]
            The language to switch the translations to.
        """
        self.translations = self.load_translation(lang)
