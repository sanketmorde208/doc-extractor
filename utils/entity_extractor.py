"""
UC8 — Named Entity Recognition (NER) on extracted <text>.
Uses spaCy if available, falls back to regex-based heuristic.
"""
import re


class EntityExtractor:
    def __init__(self):
        self._nlp = None

    def _load_nlp(self):
        if self._nlp is None:
            try:
                import spacy
                try:
                    self._nlp = spacy.load("en_core_web_sm")
                except OSError:
                    from spacy.cli import download
                    download("en_core_web_sm")
                    self._nlp = spacy.load("en_core_web_sm")
            except ImportError:
                self._nlp = "fallback"
        return self._nlp

    def extract(self, text: str) -> dict:
        nlp = self._load_nlp()

        if nlp != "fallback":
            try:
                doc = nlp(text[:100000])
                entities = {}
                for ent in doc.ents:
                    entities.setdefault(ent.label_, [])
                    if ent.text not in entities[ent.label_]:
                        entities[ent.label_].append(ent.text)
                return {
                    "PERSON": entities.get("PERSON", []),
                    "ORG": entities.get("ORG", []),
                    "GPE": entities.get("GPE", []),       # Geo-political
                    "LOC": entities.get("LOC", []),
                    "DATE": entities.get("DATE", []),
                    "MONEY": entities.get("MONEY", []),
                    "other": {k: v for k, v in entities.items()
                              if k not in ("PERSON","ORG","GPE","LOC","DATE","MONEY")},
                }
            except Exception:
                pass

        return self._regex_fallback(text)

    def _regex_fallback(self, text: str) -> dict:
        """Basic regex heuristic for common entity patterns."""
        emails = re.findall(r'\b[\w.+-]+@[\w-]+\.\w+\b', text)
        urls = re.findall(r'https?://\S+', text)
        dates = re.findall(
            r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\w+ \d{1,2},? \d{4})\b', text
        )
        money = re.findall(r'\$[\d,]+(?:\.\d{2})?|\d+(?:\.\d+)?\s?(?:USD|EUR|GBP)', text)
        # Capitalized word sequences as potential names/orgs
        names = re.findall(r'\b(?:[A-Z][a-z]+ ){1,3}[A-Z][a-z]+\b', text)

        return {
            "PERSON/ORG (heuristic)": list(set(names))[:20],
            "DATE": list(set(dates))[:20],
            "MONEY": list(set(money))[:20],
            "EMAIL": list(set(emails)),
            "URL": list(set(urls))[:10],
            "note": "Install spaCy for accurate NER: pip install spacy && python -m spacy download en_core_web_sm",
        }
