import logging

import pytest

from RAG.embeddings.vector_store import load_vector_store
from RAG.retrieval.retriever import build_retriever
from RAG.generation.llm import get_llm
from RAG.chains.rag_chain import build_rag_chain

logging.basicConfig(level=logging.INFO)


class FakeDoc:
    def __init__(self, content: str, source: str):
        self.page_content = content
        self.metadata = {"source": source}


class FakeRetriever:
    def __init__(self, docs=None, should_fail: bool = False):
        self.docs = docs or []
        self.should_fail = should_fail

    def invoke(self, question: str):
        if self.should_fail:
            raise RuntimeError("retrieval failed")

        return self.docs


class FakeLLM:
    def invoke(self, prompt_text: str):
        return "Réponse simulée"


def test_rag_chain_updates_prometheus_metrics(monkeypatch):
    from RAG.chains import rag_chain as rag_chain_module

    calls = {
        "requests": 0,
        "errors": 0,
        "retrieval": [],
        "llm": [],
        "total": [],
        "documents": [],
    }

    monkeypatch.setattr(rag_chain_module.metrics, "record_rag_request", lambda: calls.__setitem__("requests", calls["requests"] + 1))
    monkeypatch.setattr(rag_chain_module.metrics, "record_rag_error", lambda: calls.__setitem__("errors", calls["errors"] + 1))
    monkeypatch.setattr(rag_chain_module.metrics, "observe_retrieval_duration", lambda value: calls["retrieval"].append(value))
    monkeypatch.setattr(rag_chain_module.metrics, "observe_llm_duration", lambda value: calls["llm"].append(value))
    monkeypatch.setattr(rag_chain_module.metrics, "observe_total_duration", lambda value: calls["total"].append(value))
    monkeypatch.setattr(rag_chain_module.metrics, "set_retrieved_documents", lambda value: calls["documents"].append(value))

    chain = rag_chain_module.build_rag_chain(
        FakeRetriever(
            docs=[
                FakeDoc("doc 1", "source-1"),
                FakeDoc("doc 2", "source-2"),
            ]
        ),
        FakeLLM(),
    )

    result = chain.invoke("Quelle est la durée du stage ?")

    assert result["answer"] == "Réponse simulée"
    assert result["sources"] == ["source-1", "source-2"]
    assert calls["requests"] == 1
    assert calls["errors"] == 0
    assert len(calls["retrieval"]) == 1
    assert len(calls["llm"]) == 1
    assert len(calls["total"]) == 1
    assert calls["documents"] == [2]


def test_rag_chain_counts_errors_on_retrieval_failure(monkeypatch):
    from RAG.chains import rag_chain as rag_chain_module

    calls = {
        "requests": 0,
        "errors": 0,
        "retrieval": [],
        "llm": [],
        "total": [],
        "documents": [],
    }

    monkeypatch.setattr(rag_chain_module.metrics, "record_rag_request", lambda: calls.__setitem__("requests", calls["requests"] + 1))
    monkeypatch.setattr(rag_chain_module.metrics, "record_rag_error", lambda: calls.__setitem__("errors", calls["errors"] + 1))
    monkeypatch.setattr(rag_chain_module.metrics, "observe_retrieval_duration", lambda value: calls["retrieval"].append(value))
    monkeypatch.setattr(rag_chain_module.metrics, "observe_llm_duration", lambda value: calls["llm"].append(value))
    monkeypatch.setattr(rag_chain_module.metrics, "observe_total_duration", lambda value: calls["total"].append(value))
    monkeypatch.setattr(rag_chain_module.metrics, "set_retrieved_documents", lambda value: calls["documents"].append(value))

    chain = rag_chain_module.build_rag_chain(
        FakeRetriever(should_fail=True),
        FakeLLM(),
    )

    with pytest.raises(RuntimeError, match="retrieval failed"):
        chain.invoke("Question")

    assert calls["requests"] == 0
    assert calls["errors"] == 1
    assert calls["retrieval"] == []
    assert calls["llm"] == []
    assert calls["total"] == []
    assert calls["documents"] == []


def main():

    print("=" * 60)
    print("TEST DE LA CHAÎNE RAG")
    print("=" * 60)

    vectorstore = load_vector_store()

    retriever = build_retriever(vectorstore, k=4)

    llm = get_llm()

    chain = build_rag_chain(retriever, llm)

    query = "Quel est l'objectif du stage ?"

    print(f"\nQuestion : {query}\n")

    response = chain.invoke(query)

    print("Réponse :")
    print(response)

    print("=" * 60)


if __name__ == "__main__":
    main()