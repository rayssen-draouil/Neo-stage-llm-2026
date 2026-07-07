"""
vector_store.py
----------------

Création et gestion de la base vectorielle Chroma.

Responsabilités :
- créer la base vectorielle
- indexer les chunks
- recharger une base existante
- ajouter de nouveaux documents

"""

import logging
from typing import List

from langchain_chroma import Chroma
from langchain_core.documents import Document

from RAG.config import CHROMA_PERSIST_DIR
from RAG.embeddings.embedder import get_embedding_function

logger = logging.getLogger(__name__)

COLLECTION_NAME = "neoledge_docs"


def build_vector_store(chunks: List[Document]) -> Chroma:
    """
    Génère les embeddings puis indexe tous les chunks dans ChromaDB.
    """

    if not chunks:
        raise ValueError("Aucun chunk à indexer.")

    try:

        embedding_function = get_embedding_function()

        CHROMA_PERSIST_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_function,
            persist_directory=str(CHROMA_PERSIST_DIR),
            collection_name=COLLECTION_NAME,
        )

        logger.info(f"{len(chunks)} chunks indexés.")

        return vectorstore

    except Exception as e:

        logger.exception(e)

        raise RuntimeError(
            f"Erreur pendant la création de ChromaDB : {e}"
        )


def load_vector_store() -> Chroma:
    """
    Recharge une base vectorielle existante.
    """

    try:

        embedding_function = get_embedding_function()

        vectorstore = Chroma(
            persist_directory=str(CHROMA_PERSIST_DIR),
            embedding_function=embedding_function,
            collection_name=COLLECTION_NAME,
        )

        logger.info("Base vectorielle chargée.")

        return vectorstore

    except Exception as e:

        logger.exception(e)

        raise RuntimeError(
            f"Impossible de charger ChromaDB : {e}"
        )


def add_documents(
    vectorstore: Chroma,
    chunks: List[Document],
):
    """
    Ajoute de nouveaux chunks.
    """

    if not chunks:
        return

    try:

        vectorstore.add_documents(chunks)

        logger.info(
            f"{len(chunks)} nouveaux chunks ajoutés."
        )

    except Exception as e:

        logger.exception(e)

        raise RuntimeError(
            f"Erreur lors de l'ajout : {e}"
        )