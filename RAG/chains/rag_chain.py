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

PROMPT_TEMPLATE = """
Tu es un assistant documentaire NeoLedge.

Tu dois répondre UNIQUEMENT à partir du contexte fourni.

Même si tu connais la réponse grâce à tes connaissances générales,
tu dois l'ignorer.

Si la réponse n'est pas présente explicitement dans le contexte,
réponds EXACTEMENT :

"Je ne trouve pas cette information dans les documents."

Contexte :

{context}

Question :

{question}

Réponse :
"""


def format_docs(docs):

    context = "\n\n".join(doc.page_content for doc in docs)

    print("\n================ CONTEXT =================")
    print(context)
    print("==========================================\n")

    return context

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
