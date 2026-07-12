"""
rag_chain.py
------------

Chaîne RAG complète : retriever -> prompt -> LLM.
"""

import logging

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_ollama import ChatOllama

logger = logging.getLogger(__name__)

PROMPT_TEMPLATE = """Tu es un assistant qui répond aux questions en te basant uniquement sur le contexte fourni ci-dessous.
Si la réponse ne se trouve pas dans le contexte, dis-le clairement plutôt que d'inventer une réponse.

Contexte :
{context}

Question :
{question}

Réponse :"""


def format_docs(docs) -> str:
    """Concatène le contenu des documents récupérés en un seul bloc de contexte."""
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


def build_rag_chain(
    retriever: VectorStoreRetriever,
    llm: ChatOllama,
):
    """
    Construit la chaîne RAG complète avec LCEL.
    """

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    logger.info("Chaîne RAG construite.")

    return chain