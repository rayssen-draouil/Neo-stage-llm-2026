"""
main.py
-------

API FastAPI compatible OpenAI (/v1/chat/completions, /v1/embeddings)
exposant le pipeline RAG de NeoLedge.

Lancement local :
    uvicorn RAG.api.main:app --reload --port 8000

Documentation Swagger auto-générée : http://localhost:8000/docs
"""

import logging

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from RAG.api.auth import verify_token
from RAG.api.config import get_settings
from RAG.api.rag_service import embed_texts, run_rag_chain
from RAG.api.schemas import (
    ChatCompletionChoice,
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatMessage,
    EmbeddingData,
    EmbeddingsRequest,
    EmbeddingsResponse,
    ModelInfo,
    ModelsResponse,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=(
        "API REST standardisée exposant le pipeline RAG NeoLedge, "
        "compatible avec le format OpenAI."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Monitoring"])
def health_check():
    """Vérifie que l'API est disponible (aucune authentification requise)."""
    return {"status": "ok"}


@app.get(
    "/v1/models",
    response_model=ModelsResponse,
    tags=["Chat"],
)
def list_models(token: str = Depends(verify_token)):
    """
    Endpoint compatible OpenAI utilisé par Open WebUI (et autres clients)
    pour la découverte automatique des modèles disponibles.
    """
    return ModelsResponse(
        data=[
            ModelInfo(id="neoledge-rag", owned_by="neoledge"),
        ]
    )


@app.post(
    "/v1/chat/completions",
    response_model=ChatCompletionResponse,
    tags=["Chat"],
)
def chat_completions(
    request: ChatCompletionRequest,
    token: str = Depends(verify_token),
):
    """
    Endpoint compatible OpenAI. Récupère le dernier message utilisateur,
    l'envoie à la chaîne RAG (retriever -> prompt -> Qwen), et renvoie
    la réponse au format standard chat.completion.
    """
    user_messages = [m for m in request.messages if m.role == "user"]

    if not user_messages:
        raise HTTPException(
            status_code=400,
            detail="Aucun message avec le rôle 'user' n'a été fourni.",
        )

    question = user_messages[-1].content

    try:
        answer = run_rag_chain(question)
    except Exception as exc:
        logger.exception("Erreur lors de l'exécution de la chaîne RAG")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors de la génération de la réponse : {exc}",
        ) from exc

    return ChatCompletionResponse(
        model=request.model,
        choices=[
            ChatCompletionChoice(
                index=0,
                message=ChatMessage(role="assistant", content=answer),
            )
        ],
    )


@app.post(
    "/v1/embeddings",
    response_model=EmbeddingsResponse,
    tags=["Embeddings"],
)
def embeddings(
    request: EmbeddingsRequest,
    token: str = Depends(verify_token),
):
    """Endpoint compatible OpenAI pour la génération d'embeddings (nomic-embed-text)."""
    texts = request.input if isinstance(request.input, list) else [request.input]

    try:
        vectors = embed_texts(texts)
    except Exception as exc:
        logger.exception("Erreur lors de la génération des embeddings")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors de la génération des embeddings : {exc}",
        ) from exc

    data = [
        EmbeddingData(index=i, embedding=vector) for i, vector in enumerate(vectors)
    ]

    return EmbeddingsResponse(data=data, model=request.model)