"""
embedder.py
-----------

Création du modèle d'embedding via Ollama.

Le modèle utilisé est :

nomic-embed-text

Les embeddings générés serviront à :

- indexer les chunks
- embedder les questions utilisateur

"""

import logging

from langchain_ollama import OllamaEmbeddings

from RAG.config import (
    EMBEDDING_MODEL_NAME,
    OLLAMA_BASE_URL,
)

logger = logging.getLogger(__name__)


def get_embedding_function() -> OllamaEmbeddings:
    """
    Retourne le modèle d'embedding Ollama.
    """

    try:

        embedding = OllamaEmbeddings(
            model=EMBEDDING_MODEL_NAME,
            base_url=OLLAMA_BASE_URL,
        )

        logger.info(
            f"Embedding model chargé : {EMBEDDING_MODEL_NAME}"
        )

        return embedding

    except Exception as e:

        logger.exception(e)

        raise RuntimeError(
            f"Impossible de charger le modèle : {e}"
        )
