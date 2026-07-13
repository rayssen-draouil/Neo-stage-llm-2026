"""
llm.py
------

Construction du LLM Qwen via Ollama.
"""

import logging

from langchain_ollama import ChatOllama

logger = logging.getLogger(__name__)

# Ajuste le tag exact selon ce que renvoie `ollama list`
LLM_MODEL_NAME = "qwen2.5:3b"


def get_llm(temperature: float = 0) -> ChatOllama:
    """
    Retourne le client LLM Qwen pointant vers le serveur Ollama (conteneur Docker).
    """

    llm = ChatOllama(
        model=LLM_MODEL_NAME,
        temperature=temperature,
        base_url="http://localhost:11434",
    )

    logger.info(f"LLM chargé : {LLM_MODEL_NAME}")
    

    return llm

def format_docs(docs):

    context = ""

    for doc in docs:

        source = doc.metadata.get("source", "Unknown")

        page = doc.metadata.get("page", "")

        context += (
            f"\nSOURCE: {source} "
            f"(page {page})\n"
        )

        context += doc.page_content

        context += "\n\n---\n\n"

    return context