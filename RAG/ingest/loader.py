from RAG.config import PDF_FOLDER, WORD_FOLDER, MARKDOWN_FOLDER
from RAG.ingest.pdf_loader import load_pdf
from RAG.ingest.word_loader import load_word
from RAG.ingest.markdown_loader import load_markdown


def load_all_documents():
    all_documents = []

    pdf_count = 0
    word_count = 0
    md_count = 0

    for pdf in PDF_FOLDER.glob("*.pdf"):
        all_documents.extend(load_pdf(str(pdf)))
        pdf_count += 1

    for word in WORD_FOLDER.glob("*.docx"):
        all_documents.extend(load_word(str(word)))
        word_count += 1

    for md in MARKDOWN_FOLDER.glob("*.md"):
        all_documents.extend(load_markdown(str(md)))
        md_count += 1

    print(f"PDF chargés : {pdf_count}")
    print(f"Word chargés : {word_count}")
    print(f"Markdown chargés : {md_count}")
    print(f"Documents LangChain : {len(all_documents)}")

    return all_documents