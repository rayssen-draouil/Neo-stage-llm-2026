"""
rag_chain.py
------------

Chaîne RAG complète : retriever -> prompt -> LLM.
"""

import logging
from time import perf_counter
from typing import Iterable, Sequence

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_ollama import ChatOllama

from RAG.api import metrics

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


def format_docs(docs: Sequence) -> str:
    """Construit le contexte texte transmis au LLM à partir des chunks récupérés."""

    return "\n\n".join(doc.page_content for doc in docs)


def extract_sources(docs: Iterable) -> list[str]:
    """Retourne les sources uniques, dans l'ordre d'apparition, depuis les métadonnées LangChain."""

    sources: list[str] = []
    seen_sources: set[str] = set()

    for doc in docs:
        source = doc.metadata.get("source")

        if not source or source in seen_sources:
            continue

        seen_sources.add(source)
        sources.append(source)

    return sources

def build_rag_chain(
    retriever: VectorStoreRetriever,
    llm: ChatOllama,
):
    """
    Construit la chaîne RAG complète avec LCEL.
    """

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    output_parser = StrOutputParser()

    def _run(question: str) -> dict[str, object]:
        total_start = perf_counter()
        retrieved_documents = 0
        retrieval_duration = 0.0
        llm_duration = 0.0
        docs = []

        try:
            retrieval_start = perf_counter()
            docs = retriever.invoke(question)
            retrieval_duration = perf_counter() - retrieval_start

            retrieved_documents = len(docs)

            context = format_docs(docs)

            prompt_value = {
                "context": context,
                "question": question,
            }

            prompt_text = prompt.format(**prompt_value)

            llm_start = perf_counter()
            llm_response = llm.invoke(prompt_text)
            llm_duration = perf_counter() - llm_start

            response_metadata = getattr(llm_response, "response_metadata", {}) or {}

            def _ns_to_s(value: object) -> float:
                if isinstance(value, (int, float)):
                    return float(value) / 1_000_000_000

                return 0.0

            logger.info("===== OLLAMA PERFORMANCE =====")
            logger.info(
                "total_duration      : %.3f s",
                _ns_to_s(response_metadata.get("total_duration")),
            )
            logger.info(
                "load_duration       : %.3f s",
                _ns_to_s(response_metadata.get("load_duration")),
            )
            logger.info("prompt_eval_count   : %s", response_metadata.get("prompt_eval_count"))
            logger.info(
                "prompt_eval_duration: %.3f s",
                _ns_to_s(response_metadata.get("prompt_eval_duration")),
            )
            logger.info("eval_count          : %s", response_metadata.get("eval_count"))
            logger.info(
                "eval_duration       : %.3f s",
                _ns_to_s(response_metadata.get("eval_duration")),
            )
            logger.info("===============================")

            answer = output_parser.invoke(llm_response)

            metrics.record_rag_request()
            metrics.observe_retrieval_duration(retrieval_duration)
            metrics.observe_llm_duration(llm_duration)
            metrics.observe_total_duration(perf_counter() - total_start)
            metrics.set_retrieved_documents(retrieved_documents)

            return {
                "answer": answer,
                "sources": extract_sources(docs),
            }
        except Exception:
            metrics.record_rag_error()
            raise

    chain = RunnableLambda(_run)

    logger.info("Chaîne RAG construite.")

    return chain
