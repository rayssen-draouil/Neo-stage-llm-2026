"""Markdown document loader."""
from langchain_community.document_loaders import TextLoader


def load_markdown(file_path):
    """
    Charge un fichier Markdown (.md)
    """

    loader = TextLoader(file_path, encoding="utf-8")

    documents = loader.load()

    return documents