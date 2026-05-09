"""
UC9 — Translate extracted <text> to a target language.
Uses deep-translator (Google Translate API wrapper) or Argos Translate (offline).
"""


class TextTranslator:
    MAX_CHUNK = 4500  # Google Translate free limit per request

    def translate(self, text: str, target_lang: str = "es") -> str:
        if not text or not text.strip():
            return ""

        try:
            return self._google_translate(text, target_lang)
        except ImportError:
            pass
        except Exception:
            pass

        try:
            return self._argos_translate(text, target_lang)
        except ImportError:
            pass
        except Exception:
            pass

        return f"[Translation unavailable. Install: pip install deep-translator]\nOriginal: {text[:500]}"

    def _google_translate(self, text: str, target: str) -> str:
        from deep_translator import GoogleTranslator
        chunks = [text[i:i + self.MAX_CHUNK] for i in range(0, len(text), self.MAX_CHUNK)]
        translated_parts = []
        for chunk in chunks:
            result = GoogleTranslator(source="auto", target=target).translate(chunk)
            translated_parts.append(result)
        return " ".join(translated_parts)

    def _argos_translate(self, text: str, target: str) -> str:
        import argostranslate.package
        import argostranslate.translate
        from_code = "en"
        installed_languages = argostranslate.translate.get_installed_languages()
        from_lang = next((l for l in installed_languages if l.code == from_code), None)
        to_lang = next((l for l in installed_languages if l.code == target), None)
        if not from_lang or not to_lang:
            raise RuntimeError("Argos language pack not installed")
        translation = from_lang.get_translation(to_lang)
        return translation.translate(text)
