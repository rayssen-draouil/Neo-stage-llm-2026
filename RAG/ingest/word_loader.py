"""Word document loader."""
from langchain_community.document_loaders import Docx2txtLoader


def load_word(file_path):
    """
    Charge un document Word (.docx)
    """

    loader = Docx2txtLoader(file_path)

    documents = loader.load()

    return documents