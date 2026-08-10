# Neo-stage-llm-2026
# Infrastructure IA Souveraine – NeoLedge

## Description

Ce projet met en place une infrastructure IA locale basée sur un modèle LLM Open Source et un pipeline RAG (Retrieval-Augmented Generation).

L'objectif est de permettre à un assistant conversationnel de répondre à des questions en utilisant la documentation interne de NeoLedge.

Le projet repose entièrement sur des composants Open Source exécutés localement :

- Ollama
- Qwen
- nomic-embed-text
- ChromaDB
- Open WebUI
- LangChain
- Docker

---

# Architecture

```
                +----------------------+
                |   Documents          |
                | PDF / Word / MD      |
                +----------+-----------+
                           |
                           v
                 LangChain Document Loaders
                           |
                           v
                    Document Objects
                           |
                           v
         RecursiveCharacterTextSplitter
                           |
                           v
                         Chunks
                           |
                           v
          Ollama (nomic-embed-text)
                           |
                           v
                      Embeddings
                           |
                           v
                       ChromaDB
                           |
                           v
                    Semantic Retrieval
                           |
                           v
                 Ollama (Qwen 2.5)
                           |
                           v
                     Open WebUI
```

---

# Technologies

- Python 3.13
- Docker
- Docker Compose
- Ollama
- Qwen 2.5
- nomic-embed-text
- LangChain
- ChromaDB
- Open WebUI

---

# Prérequis

Installer :

- Docker Desktop
- Python 3.13+
- Git

---

# Cloner le projet

```bash
git clone <repository-url>

cd infra-ia-souveraine
```

---

# Créer l'environnement Python

Windows

```bash
python -m venv .venv
```

Activer

```bash
.venv\Scripts\activate
```

---

# Installer les dépendances

```bash
pip install -r requirements.txt
```

---

# Démarrer Docker

Lancer Docker Desktop.

Puis :

```bash
docker compose up -d
```

Vérifier :

```bash
docker ps
```

Les services suivants doivent être démarrés :

- ollama
- open-webui
- chromadb
- nginx

---

# Télécharger les modèles Ollama

Qwen

```bash
docker exec -it ollama ollama pull qwen2.5-coder:1.5b
```

Embeddings

```bash
docker exec -it ollama ollama pull nomic-embed-text
```

Vérifier

```bash
docker exec -it ollama ollama list
```

---

# Accéder à Open WebUI

```
http://localhost
```

---

# Structure du projet

```
infra-ia-souveraine/

│
├── Documents/
│      ├── pdf/
│      ├── word/
│      └── markdown/
│
├── RAG/
│      ├── ingest/
│      ├── chunking/
│      ├── embeddings/
│      ├── retrieval/
│      └── config.py
│
├── Tests/
│
├── docker-compose.yml
│
└── requirements.txt
```

---

# Pipeline RAG

Le pipeline est composé des étapes suivantes.

## 1. Ingestion

Charge automatiquement :

- PDF
- Word
- Markdown

Commande :

```bash
python -m Tests.test_loader
```

---

## 2. Chunking

Découpe les documents en chunks.

Configuration :

```
Chunk Size = 500

Chunk Overlap = 100
```

Commande :

```bash
python -m Tests.test_chunker
```

---

## 3. Embeddings

Transformation des chunks en vecteurs avec :

```
nomic-embed-text
```

Stockage dans :

```
ChromaDB
```

Commande :

```bash
python -m Tests.test_embeddings_pipeline
```

---

# Résultat attendu

```
PDF chargés : 1

Word chargés : 1

Markdown chargés : 1

Documents : 12

Chunks : 118

Embedding model chargé : nomic-embed-text

118 chunks indexés.

Question :

Quel est l'objectif du stage ?

Résultat :

Top 3 chunks trouvés.
```

---

# Configuration

Les paramètres principaux sont définis dans :

```
RAG/config.py
```

Exemple :

```python
CHUNK_SIZE = 500

CHUNK_OVERLAP = 100

EMBEDDING_MODEL_NAME = "nomic-embed-text"

OLLAMA_BASE_URL = "http://localhost:11434"
```

---

# Ports utilisés

| Service | Port |
|----------|------|
| Open WebUI | 80 |
| Ollama | 11434 |
| ChromaDB | 8000 |

---

# Vérification des services

Ollama

```bash
docker ps
```

Tester l'API

```bash
curl http://localhost:11434/api/tags
```

ChromaDB

```bash
curl http://localhost:8000/api/v2/heartbeat
```

---

# Tests

Test du chargement

```bash
python -m Tests.test_loader
```

Test du chunking

```bash
python -m Tests.test_chunker
```

Test du pipeline complet

```bash
python -m Tests.test_embeddings_pipeline
```

---

# État actuel

- ✔ Infrastructure Docker
- ✔ Ollama
- ✔ Open WebUI
- ✔ ChromaDB
- ✔ Ingestion des documents
- ✔ Chunking
- ✔ Génération des embeddings
- ✔ Indexation dans ChromaDB
- ⏳ Retrieval
- ⏳ API FastAPI
- ⏳ Intégration Open WebUI

---

# Auteur

Rayssen Draouil

Stage Été 2026

NeoLedge – Infrastructure IA Souveraine
