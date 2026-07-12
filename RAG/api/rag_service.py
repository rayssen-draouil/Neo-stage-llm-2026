"""
rag_service.py
--------------

Initialisation paresseuse (lazy, mise en cache) des composants RAG :
vectorstore Chroma, retriever, LLM Qwen et chaîne RAG complète.

Réutilise directement les modules existants du pipeline :
- RAG.retrieval.retriever.build_retriever
- RAG.generation.llm.get_llm
- RAG.chains.rag_chain.build_rag_chain
"""

import logging
from functools import lru_cache
from typing import List

from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings

from RAG.api.config import get_settings
from RAG.chains.rag_chain import build_rag_chain
from RAG.embeddings.vector_store import get_embeddings, load_vector_store
from RAG.generation.llm import get_llm
from RAG.retrieval.retriever import build_retriever

logger = logging.getLogger(__name__)


@lru_cache
def get_embeddings_model() -> OllamaEmbeddings:
    # Réutilise directement la fonction existante (RAG.embedding.vector_store),
    # qui lit déjà OLLAMA_BASE_URL / EMBEDDING_MODEL_NAME depuis RAG.config.
    return get_embeddings()


@lru_cache
def get_vectorstore() -> Chroma:
    """
    Charge la base ChromaDB persistée via la fonction d'ingestion existante,
    pour garantir un alignement total avec le pipeline (même persist_directory,
    même embeddings).
    """
    settings = get_settings()
    return load_vector_store(collection_name=settings.chroma_collection_name)


@lru_cache
def get_chain_llm() -> ChatOllama:
    settings = get_settings()
    return get_llm(temperature=settings.llm_temperature)


@lru_cache
def get_chain():
    settings = get_settings()
    retriever = build_retriever(get_vectorstore(), k=settings.retriever_k)
    llm = get_chain_llm()
    return build_rag_chain(retriever, llm)


def run_rag_chain(question: str) -> str:
    chain = get_chain()
    return chain.invoke(question)


def embed_texts(texts: List[str]) -> List[List[float]]:
    embeddings_model = get_embeddings_model()
    return embeddings_model.embed_documents(texts)
