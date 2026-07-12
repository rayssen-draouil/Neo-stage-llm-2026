"""
retriever.py
------------

Construction du retriever LangChain à partir de la base vectorielle Chroma.

Responsabilités :
- exposer un retriever configurable (k, filtres, seuil de score)
- rester découplé du reste du pipeline (chunking, embeddings, LLM)
"""

import logging

from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever

logger = logging.getLogger(__name__)


def build_retriever(
    vectorstore: Chroma,
    k: int = 4,
    search_type: str = "similarity",
) -> VectorStoreRetriever:
    """
    Construit un retriever LangChain à partir de la base vectorielle.

    search_type :
        - "similarity" : top-k par similarité
        - "mmr" : diversité des résultats (Maximal Marginal Relevance)
        - "similarity_score_threshold" : filtre par score minimal
    """

    retriever = vectorstore.as_retriever(
        search_type=search_type,
        search_kwargs={"k": k},
    )

    logger.info(
        f"Retriever construit (search_type={search_type}, k={k})"
    )

    return retriever