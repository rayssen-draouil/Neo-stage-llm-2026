"""
vector_store.py
----------------
Module de stockage vectoriel (tâche 2).

Prend en entrée les chunks produits par chunking/text_chunker.py
(Document LangChain) et les indexe dans une base vectorielle Chroma,
persistée sur disque pour survivre aux redémarrages.

Ce module est ensuite consommé par retrieval/retriever.py (tâche 3)
via l'objet Chroma retourné, qui expose similarity_search_with_score().
"""

import logging
from typing import List

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from RAG.config import CHROMA_PERSIST_DIR
from RAG.embeddings.embedder import get_embedding_function

logger = logging.getLogger(__name__)


def build_vector_store(chunks: List[Document]) -> Chroma:
    """
    Crée (ou met à jour) la base vectorielle à partir d'une liste de chunks.

    Args:
        chunks: liste de Document LangChain, sortie de
                chunking/text_chunker.py (split_documents()).

    Returns:
        Chroma: instance de la base vectorielle, persistée sur disque
                dans CHROMA_PERSIST_DIR.
    """
    if not chunks:
        raise ValueError("La liste de chunks est vide, rien à indexer.")

    try:
        embedding_function = get_embedding_function()

        CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_function,
            persist_directory=str(CHROMA_PERSIST_DIR),
        )

        logger.info(f"{len(chunks)} chunks indexés dans la base vectorielle.")
        return vectorstore

    except Exception as e:
        logger.error(f"Erreur lors de la construction de la base vectorielle : {e}")
        raise RuntimeError(f"Échec de l'indexation : {e}")


def load_vector_store() -> Chroma:
    """
    Recharge une base vectorielle déjà existante depuis le disque,
    sans re-indexer les documents. Utile au démarrage de l'API pour
    éviter de tout re-calculer à chaque redémarrage.

    Returns:
        Chroma: instance de la base vectorielle existante.
    """
    try:
        embedding_function = get_embedding_function()

        vectorstore = Chroma(
            persist_directory=str(CHROMA_PERSIST_DIR),
            embedding_function=embedding_function,
        )

        logger.info("Base vectorielle rechargée depuis le disque.")
        return vectorstore

    except Exception as e:
        logger.error(f"Erreur lors du chargement de la base vectorielle : {e}")
        raise RuntimeError(f"Échec du chargement de la base vectorielle : {e}")


def add_documents(vectorstore: Chroma, chunks: List[Document]) -> None:
    """
    Ajoute de nouveaux chunks à une base vectorielle déjà existante
    (ex: quand un nouveau document est uploadé après le démarrage).

    Args:
        vectorstore: instance Chroma déjà initialisée.
        chunks: nouveaux chunks à ajouter.
    """
    if not chunks:
        logger.warning("Aucun chunk à ajouter.")
        return

    try:
        vectorstore.add_documents(chunks)
        logger.info(f"{len(chunks)} nouveaux chunks ajoutés à la base vectorielle.")

    except Exception as e:
        logger.error(f"Erreur lors de l'ajout de documents : {e}")
        raise RuntimeError(f"Échec de l'ajout de documents : {e}")