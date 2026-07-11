"""
schemas.py
----------

Schémas Pydantic compatibles avec le format OpenAI
(/v1/chat/completions, /v1/embeddings).
"""

import time
import uuid
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Chat completions
# ---------------------------------------------------------------------------


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = Field(default="neoledge-rag")
    messages: List[ChatMessage]
    temperature: Optional[float] = None
    stream: Optional[bool] = False
    max_tokens: Optional[int] = None


class ChatCompletionChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: str = "stop"


class ChatCompletionUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class ChatCompletionResponse(BaseModel):
    id: str = Field(default_factory=lambda: f"chatcmpl-{uuid.uuid4().hex[:24]}")
    object: str = "chat.completion"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[ChatCompletionChoice]
    usage: ChatCompletionUsage = ChatCompletionUsage()


# ---------------------------------------------------------------------------
# Embeddings
# ---------------------------------------------------------------------------


class EmbeddingsRequest(BaseModel):
    model: str = Field(default="nomic-embed-text")
    input: Union[str, List[str]]


class EmbeddingData(BaseModel):
    object: str = "embedding"
    index: int
    embedding: List[float]


class EmbeddingsResponse(BaseModel):
    object: str = "list"
    data: List[EmbeddingData]
    model: str
    usage: ChatCompletionUsage = ChatCompletionUsage()


# ---------------------------------------------------------------------------
# Models (découverte, utilisée par Open WebUI)
# ---------------------------------------------------------------------------


class ModelInfo(BaseModel):
    id: str
    object: str = "model"
    created: int = Field(default_factory=lambda: int(time.time()))
    owned_by: str = "neoledge"


class ModelsResponse(BaseModel):
    object: str = "list"
    data: List[ModelInfo]