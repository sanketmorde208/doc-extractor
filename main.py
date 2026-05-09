from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

from utils.extractor import DocumentExtractor
from utils.summarizer import TextSummarizer
from utils.keyword_extractor import KeywordExtractor
from utils.table_extractor import TableExtractor
from utils.image_extractor import ImageExtractor
from utils.language_detector import LanguageDetector
from utils.sentiment_analyzer import SentimentAnalyzer
from utils.entity_extractor import EntityExtractor
from utils.translator import TextTranslator

app = FastAPI(title="Document Extraction Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

extractor = DocumentExtractor()
summarizer = TextSummarizer()
keyword_extractor = KeywordExtractor()
table_extractor = TableExtractor()
image_extractor = ImageExtractor()
language_detector = LanguageDetector()
sentiment_analyzer = SentimentAnalyzer()
entity_extractor = EntityExtractor()
translator = TextTranslator()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ─── USE CASE 1: Extract raw text from document ───────────────────────────────
@app.post("/extract/text")
async def extract_text(file: UploadFile = File(...)):
    """UC1: Extract raw <text> content from uploaded document."""
    content = await file.read()
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)

    result = extractor.extract_text(file_path, file.filename)
    return JSONResponse({
        "use_case": "Text Extraction",
        "filename": file.filename,
        "text": result["text"],          # mandatory <text> tag
        "word_count": result["word_count"],
        "char_count": result["char_count"],
    })


# ─── USE CASE 2: Summarize document text ──────────────────────────────────────
@app.post("/extract/summary")
async def summarize_document(file: UploadFile = File(...)):
    """UC2: Extract and summarize the <text> of a document."""
    content = await file.read()
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)

    raw = extractor.extract_text(file_path, file.filename)
    summary = summarizer.summarize(raw["text"])
    return JSONResponse({
        "use_case": "Document Summarization",
        "filename": file.filename,
        "text": raw["text"],             # mandatory <text> tag
        "summary": summary,
    })


# ─── USE CASE 3: Extract keywords ─────────────────────────────────────────────
@app.post("/extract/keywords")
async def extract_keywords(file: UploadFile = File(...)):
    """UC3: Extract keywords/key phrases from document <text>."""
    content = await file.read()
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)

    raw = extractor.extract_text(file_path, file.filename)
    keywords = keyword_extractor.extract(raw["text"])
    return JSONResponse({
        "use_case": "Keyword Extraction",
        "filename": file.filename,
        "text": raw["text"],             # mandatory <text> tag
        "keywords": keywords,
    })


# ─── USE CASE 4: Extract tables ───────────────────────────────────────────────
@app.post("/extract/tables")
async def extract_tables(file: UploadFile = File(...)):
    """UC4: Extract tables from PDF/DOCX documents."""
    content = await file.read()
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)

    raw = extractor.extract_text(file_path, file.filename)
    tables = table_extractor.extract(file_path, file.filename)
    return JSONResponse({
        "use_case": "Table Extraction",
        "filename": file.filename,
        "text": raw["text"],             # mandatory <text> tag
        "tables": tables,
        "table_count": len(tables),
    })


# ─── USE CASE 5: Extract images/metadata ──────────────────────────────────────
@app.post("/extract/images")
async def extract_images(file: UploadFile = File(...)):
    """UC5: Extract image metadata from documents."""
    content = await file.read()
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)

    raw = extractor.extract_text(file_path, file.filename)
    images = image_extractor.extract(file_path, file.filename)
    return JSONResponse({
        "use_case": "Image Extraction",
        "filename": file.filename,
        "text": raw["text"],             # mandatory <text> tag
        "images": images,
        "image_count": len(images),
    })


# ─── USE CASE 6: Detect language ──────────────────────────────────────────────
@app.post("/extract/language")
async def detect_language(file: UploadFile = File(...)):
    """UC6: Detect the language of the document <text>."""
    content = await file.read()
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)

    raw = extractor.extract_text(file_path, file.filename)
    lang = language_detector.detect(raw["text"])
    return JSONResponse({
        "use_case": "Language Detection",
        "filename": file.filename,
        "text": raw["text"],             # mandatory <text> tag
        "language": lang["language"],
        "confidence": lang["confidence"],
    })


# ─── USE CASE 7: Sentiment analysis ───────────────────────────────────────────
@app.post("/extract/sentiment")
async def analyze_sentiment(file: UploadFile = File(...)):
    """UC7: Perform sentiment analysis on document <text>."""
    content = await file.read()
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)

    raw = extractor.extract_text(file_path, file.filename)
    sentiment = sentiment_analyzer.analyze(raw["text"])
    return JSONResponse({
        "use_case": "Sentiment Analysis",
        "filename": file.filename,
        "text": raw["text"],             # mandatory <text> tag
        "sentiment": sentiment["label"],
        "score": sentiment["score"],
    })


# ─── USE CASE 8: Named entity recognition ─────────────────────────────────────
@app.post("/extract/entities")
async def extract_entities(file: UploadFile = File(...)):
    """UC8: Extract named entities (persons, orgs, locations) from <text>."""
    content = await file.read()
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)

    raw = extractor.extract_text(file_path, file.filename)
    entities = entity_extractor.extract(raw["text"])
    return JSONResponse({
        "use_case": "Named Entity Recognition",
        "filename": file.filename,
        "text": raw["text"],             # mandatory <text> tag
        "entities": entities,
    })


# ─── USE CASE 9: Translate document text ──────────────────────────────────────
@app.post("/extract/translate")
async def translate_text(file: UploadFile = File(...), target_lang: str = "es"):
    """UC9: Translate the <text> of a document to a target language."""
    content = await file.read()
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)

    raw = extractor.extract_text(file_path, file.filename)
    translated = translator.translate(raw["text"], target_lang)
    return JSONResponse({
        "use_case": "Text Translation",
        "filename": file.filename,
        "text": raw["text"],             # mandatory <text> tag
        "translated_text": translated,
        "target_language": target_lang,
    })


# ─── Health check ─────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok", "service": "Document Extraction Platform"}


# ─── Serve UI ─────────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def root():
    with open("templates/index.html") as f:
        return f.read()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
