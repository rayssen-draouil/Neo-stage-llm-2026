"""
metrics.py
----------

Métriques Prometheus partagées par l'API RAG.
"""

from __future__ import annotations

from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram, REGISTRY


def _get_or_create_metric(metric_cls, name: str, documentation: str):
    existing = REGISTRY._names_to_collectors.get(name)
    if existing is not None:
        return existing

    return metric_cls(name, documentation)


rag_requests_total = _get_or_create_metric(
    Counter,
    "rag_requests_total",
    "Nombre total de requêtes RAG",
)
rag_errors_total = _get_or_create_metric(
    Counter,
    "rag_errors_total",
    "Nombre total de requêtes RAG en erreur",
)
rag_retrieval_duration_seconds = _get_or_create_metric(
    Histogram,
    "rag_retrieval_duration_seconds",
    "Durée du retrieval RAG en secondes",
)
rag_llm_duration_seconds = _get_or_create_metric(
    Histogram,
    "rag_llm_duration_seconds",
    "Durée de génération LLM en secondes",
)
rag_total_duration_seconds = _get_or_create_metric(
    Histogram,
    "rag_total_duration_seconds",
    "Durée totale du pipeline RAG en secondes",
)
rag_retrieved_documents = _get_or_create_metric(
    Gauge,
    "rag_retrieved_documents",
    "Nombre de documents récupérés lors de la dernière exécution RAG",
)


def record_rag_request() -> None:
    rag_requests_total.inc()


def record_rag_error() -> None:
    rag_errors_total.inc()


def observe_retrieval_duration(duration_seconds: float) -> None:
    rag_retrieval_duration_seconds.observe(duration_seconds)


def observe_llm_duration(duration_seconds: float) -> None:
    rag_llm_duration_seconds.observe(duration_seconds)


def observe_total_duration(duration_seconds: float) -> None:
    rag_total_duration_seconds.observe(duration_seconds)


def set_retrieved_documents(count: int) -> None:
    rag_retrieved_documents.set(count)