"""
Gestion du vector store ChromaDB avec embeddings Ollama.
"""

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from RAG.config import CHROMA_PERSIST_DIR, OLLAMA_BASE_URL, EMBEDDING_MODEL_NAME


def get_embeddings():
    """Retourne le modèle d'embeddings Ollama."""
    return OllamaEmbeddings(
        base_url=OLLAMA_BASE_URL,
        model=EMBEDDING_MODEL_NAME,
    )


def load_vector_store(collection_name: str = "neoledge_docs"):
    """
    Charge le vector store ChromaDB existant depuis le dossier de persistance.
    Le vector store doit avoir été créé au préalable via ingest.
    """
    embeddings = get_embeddings()

    vectorstore = Chroma(
        collection_name=collection_name,
        persist_directory=str(CHROMA_PERSIST_DIR),
        embedding_function=embeddings,
    )

    count = vectorstore._collection.count()
    print(f"Vector store chargé : {count} chunks dans ChromaDB")

    return vectorstore


def build_vector_store(documents):
    """
    Crée et persiste un vector store ChromaDB à partir d'une liste de documents LangChain.
    À utiliser lors de l'ingestion initiale.
    """
    embeddings = get_embeddings()

    CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=str(CHROMA_PERSIST_DIR),
    )

    print(f"Vector store créé : {vectorstore._collection.count()} chunks indexés")

    return vectorstore
