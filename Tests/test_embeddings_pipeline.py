import logging

from RAG.ingest.loader import load_all_documents
from RAG.chunking.text_chunker import split_documents
from RAG.embeddings.vector_store import build_vector_store

logging.basicConfig(level=logging.INFO)


def main():

    print("=" * 60)
    print("TEST DU PIPELINE EMBEDDINGS")
    print("=" * 60)

    # -----------------------
    # Chargement
    # -----------------------

    documents = load_all_documents()

    print(f"\nDocuments chargés : {len(documents)}")

    # -----------------------
    # Chunking
    # -----------------------

    chunks = split_documents(documents)

    print(f"Chunks générés : {len(chunks)}")

    # -----------------------
    # Embeddings
    # -----------------------

    print("\nCréation de la base vectorielle...")

    vectorstore = build_vector_store(chunks)

    print("Base vectorielle créée avec succès.")

    # -----------------------
    # Recherche
    # -----------------------

    query = "Quel est l'objectif du stage ?"

    print("\nQuestion de test :")

    print(query)

    results = vectorstore.similarity_search_with_score(
        query,
        k=3,
    )

    print("\nRésultats :")

    for index, (doc, score) in enumerate(results, start=1):

        print("-" * 60)

        print(f"Résultat {index}")

        print(f"Score : {score:.4f}")

        print(
            f"Source : {doc.metadata.get('source')}"
        )

        print(
            f"Page : {doc.metadata.get('page')}"
        )

        print("\nExtrait :\n")

        print(doc.page_content[:300])

        print()

    print("=" * 60)
    print("TEST TERMINÉ")
    print("=" * 60)


if __name__ == "__main__":
    main()