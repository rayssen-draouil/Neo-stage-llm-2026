from RAG.ingest.loader import load_all_documents
from RAG.chunking.text_chunker import split_documents
documents = load_all_documents()

print(f"Nombre total de documents chargés : {len(documents)}")
for doc in documents[:5]:
    print("-" * 40)
    #print(doc)
    print( type(doc))
    print("-" * 40)
chunked_documents = split_documents(documents)
#print(chunked_documents)
print("Number of chunks:", len(chunked_documents))

print("\nSample chunk:\n")
print(chunked_documents[0].page_content[:500])

print("\nMetadata:\n")
print(chunked_documents[0].metadata)