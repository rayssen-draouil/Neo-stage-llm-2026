from RAG.ingest.loader import load_all_documents

documents = load_all_documents()

print(f"Nombre total de documents chargés : {len(documents)}")

for doc in documents[:5]:
    print("-" * 40)
    print(doc.metadata)