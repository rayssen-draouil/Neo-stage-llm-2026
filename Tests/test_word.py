from RAG.config import WORD_FOLDER
from RAG.ingest.word_loader import load_word

word_path = WORD_FOLDER / "enonce stage w.docx"

documents = load_word(str(word_path))

print(f"Nombre de documents : {len(documents)}")

print("\n===== Contenu =====\n")
print(documents[0].page_content)

print("\n===== Métadonnées =====\n")
print(documents[0].metadata)