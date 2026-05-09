"""
UC2 — Summarize extracted <text> using transformers or fallback extractive method.
"""
import re


class TextSummarizer:
    def __init__(self):
        self._pipeline = None

    def _load_pipeline(self):
        if self._pipeline is None:
            try:
                from transformers import pipeline
                self._pipeline = pipeline(
                    "summarization",
                    model="facebook/bart-large-cnn",
                    max_length=200,
                    min_length=40,
                    do_sample=False,
                )
            except Exception:
                self._pipeline = "fallback"
        return self._pipeline

    def summarize(self, text: str) -> str:
        if not text or len(text.strip()) < 50:
            return text

        pipeline = self._load_pipeline()

        if pipeline == "fallback":
            return self._extractive_summary(text)

        # HuggingFace BART supports up to ~1024 tokens; chunk if needed
        chunk = text[:3000]
        try:
            result = pipeline(chunk)
            return result[0]["summary_text"]
        except Exception:
            return self._extractive_summary(text)

    def _extractive_summary(self, text: str, sentences: int = 3) -> str:
        """Simple extractive summary — first N sentences."""
        sent = re.split(r'(?<=[.!?])\s+', text.strip())
        return " ".join(sent[:sentences])
