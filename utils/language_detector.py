"""
UC6 — Detect the language of extracted <text>.
Uses langdetect; falls back to a simple heuristic.
"""


class LanguageDetector:
    def detect(self, text: str) -> dict:
        if not text or len(text.strip()) < 10:
            return {"language": "unknown", "confidence": 0.0}

        try:
            from langdetect import detect, detect_langs
            langs = detect_langs(text)
            top = langs[0]
            return {
                "language": top.lang,
                "confidence": round(top.prob, 4),
                "all_candidates": [{"lang": l.lang, "prob": round(l.prob, 4)} for l in langs],
            }
        except ImportError:
            return self._heuristic_detect(text)
        except Exception as e:
            return {"language": "unknown", "confidence": 0.0, "error": str(e)}

    def _heuristic_detect(self, text: str) -> dict:
        """Very simple ASCII heuristic — defaults to English."""
        ascii_ratio = sum(1 for c in text if ord(c) < 128) / max(len(text), 1)
        if ascii_ratio > 0.95:
            return {"language": "en", "confidence": 0.7, "note": "heuristic"}
        return {"language": "unknown", "confidence": 0.3, "note": "heuristic"}
