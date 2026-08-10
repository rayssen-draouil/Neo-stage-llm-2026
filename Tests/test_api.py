"""
test_api.py
-----------

Tests d'intégration de l'API FastAPI :
- Tests d'authentification (rapides, sans dépendance externe)
- Tests fonctionnels des endpoints /v1/chat/completions et /v1/embeddings
  (marqués "integration" : nécessitent Ollama + ChromaDB actifs)

Lancer tous les tests rapides :
    pytest Tests/test_api.py

Lancer aussi les tests d'intégration réels :
    pytest Tests/test_api.py -m integration
"""

import os

os.environ.setdefault("API_TOKEN", "test-token")

import pytest
from fastapi.testclient import TestClient

from RAG.api.main import app

client = TestClient(app)
VALID_TOKEN = os.environ["API_TOKEN"]


def auth_header(token: str = VALID_TOKEN) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_health_check_no_auth_required():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_metrics_endpoint_exposes_prometheus_text():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    body = response.text
    assert "rag_requests_total" in body
    assert "rag_errors_total" in body
    assert "rag_retrieval_duration_seconds" in body
    assert "rag_llm_duration_seconds" in body
    assert "rag_total_duration_seconds" in body
    assert "rag_retrieved_documents" in body


def test_chat_completions_rejects_missing_token():
    response = client.post(
        "/v1/chat/completions",
        json={"messages": [{"role": "user", "content": "Bonjour"}]},
    )
    assert response.status_code == 401


def test_chat_completions_rejects_invalid_token():
    response = client.post(
        "/v1/chat/completions",
        json={"messages": [{"role": "user", "content": "Bonjour"}]},
        headers=auth_header("mauvais-token"),
    )
    assert response.status_code == 401


def test_chat_completions_rejects_empty_messages():
    response = client.post(
        "/v1/chat/completions",
        json={"messages": []},
        headers=auth_header(),
    )
    assert response.status_code == 400


def test_embeddings_rejects_missing_token():
    response = client.post(
        "/v1/embeddings",
        json={"input": "test"},
    )
    assert response.status_code == 401


def test_chat_completions_exposes_answer_and_sources(monkeypatch):
    monkeypatch.setattr(
        "RAG.api.main.run_rag_chain",
        lambda question: (
            "Le stage dure 9 semaines.",
            [
                r"C:\rayssen\Stage Neoledge\2026\infra-ia-souveraine\Documents\markdown\enonce stage.md",
                r"C:\rayssen\Stage Neoledge\2026\infra-ia-souveraine\Documents\word\enonce stage.docx",
            ],
        ),
    )

    response = client.post(
        "/v1/chat/completions",
        json={"messages": [{"role": "user", "content": "Quelle est la durée du stage ?"}]},
        headers=auth_header(),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["answer"] == "Le stage dure 9 semaines."
    assert payload["sources"] == [
        r"C:\rayssen\Stage Neoledge\2026\infra-ia-souveraine\Documents\markdown\enonce stage.md",
        r"C:\rayssen\Stage Neoledge\2026\infra-ia-souveraine\Documents\word\enonce stage.docx",
    ]
    assert payload["choices"][0]["message"]["content"] == (
        "Le stage dure 9 semaines.\n\n---\nSources :\n"
        "- markdown/enonce stage.md\n"
        "- word/enonce stage.docx"
    )


def test_chat_completions_formats_document_relative_paths(monkeypatch):
    monkeypatch.setattr(
        "RAG.api.main.run_rag_chain",
        lambda question: (
            "La durée du stage est de 9 semaines.",
            [
                r"C:\rayssen\Stage Neoledge\2026\infra-ia-souveraine\Documents\pdf\specification.pdf",
                r"C:\rayssen\Stage Neoledge\2026\infra-ia-souveraine\Documents\markdown\enonce stage - t.md",
                r"C:\rayssen\Stage Neoledge\2026\infra-ia-souveraine\temp\notes.txt",
            ],
        ),
    )

    response = client.post(
        "/v1/chat/completions",
        json={"messages": [{"role": "user", "content": "Quelle est la durée du stage ?"}]},
        headers=auth_header(),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["choices"][0]["message"]["content"] == (
        "La durée du stage est de 9 semaines.\n\n---\nSources :\n"
        "- pdf/specification.pdf\n"
        "- markdown/enonce stage - t.md\n"
        "- notes.txt"
    )


def test_chat_completions_keeps_raw_answer_when_no_sources(monkeypatch):
    monkeypatch.setattr(
        "RAG.api.main.run_rag_chain",
        lambda question: ("Le stage dure 9 semaines.", []),
    )

    response = client.post(
        "/v1/chat/completions",
        json={"messages": [{"role": "user", "content": "Quelle est la durée du stage ?"}]},
        headers=auth_header(),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["answer"] == "Le stage dure 9 semaines."
    assert payload["sources"] == []
    assert payload["choices"][0]["message"]["content"] == payload["answer"]


@pytest.mark.integration
def test_chat_completions_returns_valid_openai_format():
    """Nécessite Ollama (Qwen) + ChromaDB peuplé et accessibles."""
    response = client.post(
        "/v1/chat/completions",
        json={
            "messages": [
                {"role": "user", "content": "Quel est l'objectif du stage ?"}
            ]
        },
        headers=auth_header(),
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["object"] == "chat.completion"
    assert payload["choices"][0]["message"]["role"] == "assistant"
    assert len(payload["choices"][0]["message"]["content"]) > 0
    assert isinstance(payload["sources"], list)


@pytest.mark.integration
def test_embeddings_returns_valid_openai_format():
    """Nécessite Ollama (nomic-embed-text) accessible."""
    response = client.post(
        "/v1/embeddings",
        json={"input": "Texte de test pour l'embedding."},
        headers=auth_header(),
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["object"] == "list"
    assert len(payload["data"]) == 1
    assert len(payload["data"][0]["embedding"]) > 0
