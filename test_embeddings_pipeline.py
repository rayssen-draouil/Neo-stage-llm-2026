"""
test_embeddings_pipeline.py
-----------------------------
Script de validation rapide du module embeddings (tâche 2).

Usage :
    py test_embeddings_pipeline.py
"""

import logging

from RAG.ingest.loader import load_all_documents
from RAG.chunking.text_chunker import split_documents
from RAG.embeddings.vector_store import build_vector_store

logging.basicConfig(level=logging.INFO)


def main():
    print("=" * 50)
    print("Test du pipeline Embeddings")
    print("=" * 50)

    # Étape 1 : charger les documents (PDF/Word/Markdown dans Documents/)
    documents = load_all_documents()
    if not documents:
        print("Aucun document trouvé. Place un fichier de test dans Documents/pdf/, "
              "Documents/word/ ou Documents/markdown/.")
        return

    # Étape 2 : découper en chunks
    chunks = split_documents(documents)

    # Étape 3 : générer les embeddings et indexer
    vectorstore = build_vector_store(chunks)

    # Étape 4 : test de recherche rapide
    query = "Résume le contenu du document."
    results = vectorstore.similarity_search_with_score(query, k=3)

    print("\n" + "=" * 50)
    print("Test de recherche")
    print("=" * 50)
    for doc, score in results:
        print(f"\nScore (distance) : {score:.4f}")
        print(f"Source : {doc.metadata.get('source', 'inconnu')}")
        print(f"Extrait : {doc.page_content[:150]}...")


if __name__ == "__main__":
    main()