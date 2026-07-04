"""PDF document loader."""
from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path):
    """
    Charge un PDF et retourne une liste de documents LangChain.
    """

    loader = PyPDFLoader(file_path)

    documents = loader.load()

    return documents