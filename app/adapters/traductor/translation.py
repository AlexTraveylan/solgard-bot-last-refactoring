import json
from typing import Literal


class Translate:
    def __init__(self, lang: Literal["fr", "en", "it", "es", "zh", "ru"]) -> None:
        self.lang = lang
        self.translations = self.load_translation(lang)

    def load_translation(self, lang: Literal["fr", "en", "it", "es", "zh", "ru"]) -> dict[str, str]:
        try:
            with open(f"app/adapters/traductor/{lang}.json", encoding="utf-8") as lang_file:
                translations = json.load(lang_file)
                return translations
        except FileNotFoundError:
            raise ValueError(f"Failed to find {lang}.json")
        except json.JSONDecodeError:
            raise ValueError(f"Failed to decode {lang}.json")

    def set_translation(self, lang: Literal["fr", "en", "it", "es", "zh", "ru"]):
        self.translations = self.load_translation(lang)
