"""
UC3 — Extract keywords/key phrases from <text>.
Uses KeyBERT if available, falls back to TF-IDF style extraction.
"""
import re
from collections import Counter


class KeywordExtractor:
    def __init__(self):
        self._model = None

    def _load_model(self):
        if self._model is None:
            try:
                from keybert import KeyBERT
                self._model = KeyBERT()
            except ImportError:
                self._model = "fallback"
        return self._model

    def extract(self, text: str, top_n: int = 15) -> list:
        model = self._load_model()

        if model != "fallback":
            try:
                kws = model.extract_keywords(
                    text,
                    keyphrase_ngram_range=(1, 2),
                    stop_words="english",
                    top_n=top_n,
                )
                return [{"keyword": kw, "score": round(score, 4)} for kw, score in kws]
            except Exception:
                pass

        return self._fallback_keywords(text, top_n)

    def _fallback_keywords(self, text: str, top_n: int) -> list:
        STOPWORDS = {
            "the","a","an","and","or","but","in","on","at","to","for","of","with",
            "is","are","was","were","be","been","being","have","has","had","do",
            "does","did","will","would","could","should","may","might","shall",
            "this","that","these","those","i","you","he","she","it","we","they",
            "what","which","who","how","when","where","why","not","no","so","if",
        }
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        filtered = [w for w in words if w not in STOPWORDS]
        counts = Counter(filtered).most_common(top_n)
        total = sum(c for _, c in counts) or 1
        return [{"keyword": w, "score": round(c / total, 4)} for w, c in counts]
