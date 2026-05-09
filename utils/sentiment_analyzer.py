"""
UC7 — Sentiment analysis on extracted <text>.
Uses HuggingFace transformers pipeline or TextBlob fallback.
"""


class SentimentAnalyzer:
    def __init__(self):
        self._pipeline = None

    def _load_pipeline(self):
        if self._pipeline is None:
            try:
                from transformers import pipeline
                self._pipeline = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    truncation=True,
                    max_length=512,
                )
            except Exception:
                self._pipeline = "fallback"
        return self._pipeline

    def analyze(self, text: str) -> dict:
        if not text or len(text.strip()) < 5:
            return {"label": "NEUTRAL", "score": 0.5}

        pipeline = self._load_pipeline()

        if pipeline != "fallback":
            try:
                result = pipeline(text[:512])[0]
                return {"label": result["label"], "score": round(result["score"], 4)}
            except Exception:
                pass

        return self._textblob_fallback(text)

    def _textblob_fallback(self, text: str) -> dict:
        try:
            from textblob import TextBlob
            polarity = TextBlob(text).sentiment.polarity
            if polarity > 0.1:
                label, score = "POSITIVE", round((polarity + 1) / 2, 4)
            elif polarity < -0.1:
                label, score = "NEGATIVE", round((1 - polarity) / 2, 4)
            else:
                label, score = "NEUTRAL", 0.5
            return {"label": label, "score": score}
        except ImportError:
            # Pure heuristic
            pos = sum(text.lower().count(w) for w in ["good","great","excellent","amazing","positive","happy"])
            neg = sum(text.lower().count(w) for w in ["bad","poor","terrible","negative","awful","sad"])
            if pos > neg:
                return {"label": "POSITIVE", "score": 0.65}
            elif neg > pos:
                return {"label": "NEGATIVE", "score": 0.65}
            return {"label": "NEUTRAL", "score": 0.5}
