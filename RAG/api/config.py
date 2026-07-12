"""
config.py
---------

Configuration de l'API via variables d'environnement (voir .env.example).
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Sécurité
    api_token: str = "changeme-token"

    # ChromaDB
    # NB : le persist_directory et les embeddings sont gérés par
    # RAG.embedding.vector_store (donc par RAG.config), pas besoin de les
    # dupliquer ici. Seul le nom de la collection est piloté par l'API.
    chroma_collection_name: str = "neoledge_docs"

    # Ollama (utilisés uniquement si besoin de recréer un client LLM/embeddings
    # indépendant ; RAG.embedding.vector_store gère déjà les siens)
    ollama_base_url: str = "http://localhost:11434"
    embedding_model: str = "nomic-embed-text"
    llm_model: str = "qwen2.5:3b"

    # RAG
    retriever_k: int = 4
    llm_temperature: float = 0.1

    # Métadonnées API
    api_title: str = "NeoLedge RAG API"
    api_version: str = "1.0.0"


@lru_cache
def get_settings() -> Settings:
    return Settings()
