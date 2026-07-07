"""
embedder.py
-----------
Module de génération des embeddings (tâche 2).

Fournit le modèle d'embedding utilisé pour transformer :
- les chunks de documents (à l'indexation)
- les questions utilisateur (à la recherche)

Utilise le même modèle des deux côtés (obligatoire pour que la
similarité vectorielle ait un sens), conformément au cahier des
charges : BAAI/bge-small-en-v1.5 via sentence-transformers.
"""

import logging

from langchain_huggingface import HuggingFaceEmbeddings

from RAG.config import EMBEDDING_MODEL_NAME

logger = logging.getLogger(__name__)


def get_embedding_function() -> HuggingFaceEmbeddings:
    """
    Retourne une instance LangChain-compatible du modèle d'embedding.

    Cette fonction est le point d'entrée unique utilisé par :
    - vector_store.py (tâche 2) pour indexer les chunks
    - retrieval/retriever.py (tâche 3) si besoin d'embedder une question

    Returns:
        HuggingFaceEmbeddings: objet embedding compatible avec Chroma,
        Qdrant, FAISS, etc.
    """
    try:
        embedding_function = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            model_kwargs={"device": "cpu"},  # pas de GPU disponible sur la machine
            encode_kwargs={"normalize_embeddings": True},  # recommandé pour bge-*
        )
        logger.info(f"Modèle d'embedding chargé : {EMBEDDING_MODEL_NAME}")
        return embedding_function

    except Exception as e:
        logger.error(f"Erreur lors du chargement du modèle d'embedding : {e}")
        raise RuntimeError(f"Impossible de charger le modèle d'embedding : {e}")