"""
Configuration du projet RAG
"""

from pathlib import Path

# Racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Dossiers des documents
PDF_FOLDER = BASE_DIR / "Documents" / "pdf"
WORD_FOLDER = BASE_DIR / "Documents" / "word"
MARKDOWN_FOLDER = BASE_DIR / "Documents" / "markdown"

# Extensions supportées
SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".md"
}
# ==========================
# Chunking Configuration
# ==========================

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100