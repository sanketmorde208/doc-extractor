"""
UC5 — Extract image metadata from PDF and DOCX documents.
"""


class ImageExtractor:
    def extract(self, file_path: str, filename: str) -> list:
        ext = filename.lower().split(".")[-1]
        if ext == "pdf":
            return self._extract_pdf_images(file_path)
        elif ext in ("docx", "doc"):
            return self._extract_docx_images(file_path)
        return []

    def _extract_pdf_images(self, path: str) -> list:
        try:
            import pdfplumber
            images = []
            with pdfplumber.open(path) as pdf:
                for i, page in enumerate(pdf.pages):
                    for j, img in enumerate(page.images):
                        images.append({
                            "page": i + 1,
                            "image_index": j + 1,
                            "width": img.get("width"),
                            "height": img.get("height"),
                            "x0": img.get("x0"),
                            "y0": img.get("y0"),
                            "colorspace": img.get("colorspace"),
                        })
            return images
        except ImportError:
            return [{"error": "pdfplumber not installed"}]
        except Exception as e:
            return [{"error": str(e)}]

    def _extract_docx_images(self, path: str) -> list:
        try:
            from docx import Document
            import zipfile, os
            images = []
            with zipfile.ZipFile(path, "r") as z:
                media_files = [f for f in z.namelist() if f.startswith("word/media/")]
                for i, mf in enumerate(media_files):
                    info = z.getinfo(mf)
                    images.append({
                        "image_index": i + 1,
                        "filename": os.path.basename(mf),
                        "size_bytes": info.file_size,
                        "compressed_bytes": info.compress_size,
                    })
            return images
        except Exception as e:
            return [{"error": str(e)}]
