"""
UC1 Core Utility — extracts raw <text> from PDF, DOCX, TXT files.
"""
import os


class DocumentExtractor:
    def extract_text(self, file_path: str, filename: str) -> dict:
        ext = filename.lower().split(".")[-1]

        if ext == "pdf":
            text = self._extract_pdf(file_path)
        elif ext in ("docx", "doc"):
            text = self._extract_docx(file_path)
        elif ext == "txt":
            text = self._extract_txt(file_path)
        elif ext in ("png", "jpg", "jpeg", "tiff", "bmp"):
            text = self._extract_image_ocr(file_path)
        else:
            raise ValueError(f"Unsupported file type: .{ext}")

        return {
            "text": text.strip(),
            "word_count": len(text.split()),
            "char_count": len(text),
        }

    # ── PDF ────────────────────────────────────────────────────────────────────
    def _extract_pdf(self, path: str) -> str:
        try:
            import pdfplumber
            text_parts = []
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        text_parts.append(t)
            return "\n".join(text_parts)
        except ImportError:
            import PyPDF2
            text_parts = []
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    t = page.extract_text()
                    if t:
                        text_parts.append(t)
            return "\n".join(text_parts)

    # ── DOCX ───────────────────────────────────────────────────────────────────
    def _extract_docx(self, path: str) -> str:
        from docx import Document
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    # ── TXT ────────────────────────────────────────────────────────────────────
    def _extract_txt(self, path: str) -> str:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    # ── IMAGE OCR ──────────────────────────────────────────────────────────────
    def _extract_image_ocr(self, path: str) -> str:
        try:
            import pytesseract
            from PIL import Image
            img = Image.open(path)
            return pytesseract.image_to_string(img)
        except ImportError:
            return "[OCR unavailable: install pytesseract and Pillow]"
