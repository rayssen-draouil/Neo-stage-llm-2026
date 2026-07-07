# RAG/chunking/text_chunker.py

from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(
    documents,
    chunk_size=800,
    chunk_overlap=200,
):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    return chunks

# TODO:
# - text normalization / cleaning (whitespace, headers, footers)
# - improve chunking strategy (semantic / structure-aware)