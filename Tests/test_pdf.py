from RAG.config import PDF_FOLDER
from RAG.ingest.pdf_loader import load_pdf

pdf_path = PDF_FOLDER / "enonce stage.pdf"

documents = load_pdf(str(pdf_path))

print(f"Nombre de pages : {len(documents)}")

print("\n===== Première page =====\n")
print(documents[0].page_content)

print("\n===== Métadonnées =====\n")
print(documents[0].metadata)