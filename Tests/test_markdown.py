from RAG.config import MARKDOWN_FOLDER
from RAG.ingest.markdown_loader import load_markdown

md_path = MARKDOWN_FOLDER / "enonce stage - t.md"

documents = load_markdown(str(md_path))

print(f"Nombre de documents : {len(documents)}")

print("\n===== Contenu =====\n")
print(documents[0].page_content)

print("\n===== Métadonnées =====\n")
print(documents[0].metadata)