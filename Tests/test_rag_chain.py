import logging

from RAG.embeddings.vector_store import load_vector_store
from RAG.retrieval.retriever import build_retriever
from RAG.generation.llm import get_llm
from RAG.chains.rag_chain import build_rag_chain

logging.basicConfig(level=logging.INFO)


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