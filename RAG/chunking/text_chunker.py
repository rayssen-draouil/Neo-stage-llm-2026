from langchain_text_splitters import RecursiveCharacterTextSplitter
from RAG.config import CHUNK_SIZE, CHUNK_OVERLAP


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(documents)

    print("=" * 50)
    print("Chunking Summary")
    print("=" * 50)
    print(f"Input documents : {len(documents)}")
    print(f"Output chunks    : {len(chunks)}")
    print(f"Chunk size       : {CHUNK_SIZE}")
    print(f"Chunk overlap    : {CHUNK_OVERLAP}")

    return chunks