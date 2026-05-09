"""
UC4 — Extract tables from PDF and DOCX documents.
"""


class TableExtractor:
    def extract(self, file_path: str, filename: str) -> list:
        ext = filename.lower().split(".")[-1]
        if ext == "pdf":
            return self._extract_pdf_tables(file_path)
        elif ext in ("docx", "doc"):
            return self._extract_docx_tables(file_path)
        return []

    def _extract_pdf_tables(self, path: str) -> list:
        try:
            import pdfplumber
            tables = []
            with pdfplumber.open(path) as pdf:
                for i, page in enumerate(pdf.pages):
                    for j, table in enumerate(page.extract_tables()):
                        if table:
                            tables.append({
                                "page": i + 1,
                                "table_index": j + 1,
                                "rows": len(table),
                                "columns": len(table[0]) if table else 0,
                                "data": table,
                            })
            return tables
        except ImportError:
            return [{"error": "pdfplumber not installed. Run: pip install pdfplumber"}]
        except Exception as e:
            return [{"error": str(e)}]

    def _extract_docx_tables(self, path: str) -> list:
        try:
            from docx import Document
            doc = Document(path)
            tables = []
            for i, table in enumerate(doc.tables):
                data = []
                for row in table.rows:
                    data.append([cell.text.strip() for cell in row.cells])
                tables.append({
                    "table_index": i + 1,
                    "rows": len(data),
                    "columns": len(data[0]) if data else 0,
                    "data": data,
                })
            return tables
        except ImportError:
            return [{"error": "python-docx not installed. Run: pip install python-docx"}]
        except Exception as e:
            return [{"error": str(e)}]
