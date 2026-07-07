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
# ==========================
# Embeddings Configuration
# ==========================
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"

# ==========================
# Vector Store Configuration
# ==========================
CHROMA_PERSIST_DIR = BASE_DIR / "storage" / "chroma_db"