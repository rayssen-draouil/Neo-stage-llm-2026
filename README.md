# 🚀 Infrastructure IA Souveraine – NeoLedge

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)]()
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)]()
[![LangChain](https://img.shields.io/badge/LangChain-RAG-green.svg)]()
[![OpenWebUI](https://img.shields.io/badge/OpenWebUI-Integrated-orange.svg)]()
[![License](https://img.shields.io/badge/License-Internal-red.svg)]()

---

# 📖 Description

Ce projet a pour objectif de mettre en place une **infrastructure IA souveraine entièrement locale** basée sur des modèles Open Source.

La solution permet d'interroger la documentation interne de NeoLedge grâce à un pipeline **RAG (Retrieval-Augmented Generation)** afin de fournir des réponses contextualisées tout en garantissant :

- 🔒 Confidentialité des données
- 🏠 Exécution 100% locale
- ☁️ Aucune dépendance à un fournisseur cloud
- 🔁 Déploiement reproductible via Docker
- 🔌 Compatibilité avec l'API OpenAI
- 🤖 Intégration native avec Open WebUI

---

# ✨ Fonctionnalités

## 📄 Ingestion documentaire

Support automatique de :

- PDF
- Word (.docx)
- Markdown (.md)

---

## 🧠 Pipeline RAG complet

- Extraction documentaire
- Découpage en chunks
- Génération d'embeddings
- Indexation vectorielle
- Recherche sémantique
- Génération augmentée par récupération documentaire

---

## 🤖 IA locale

- Ollama
- Qwen 2.5
- nomic-embed-text
- ChromaDB
- Open WebUI

---

## 🌐 API REST compatible OpenAI

Endpoints disponibles :

- `/v1/chat/completions`
- `/v1/embeddings`
- `/v1/models`

---

# 🏗 Architecture Globale

```text
                         ┌──────────────────────┐
                         │ Internal Documents   │
                         │ PDF / Word / MD      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    LangChain Document Loaders
                                    │
                                    ▼
                           Document Objects
                                    │
                                    ▼
                RecursiveCharacterTextSplitter
                                    │
                                    ▼
                                  Chunks
                                    │
                                    ▼
                     Ollama (nomic-embed-text)
                                    │
                                    ▼
                                Embeddings
                                    │
                                    ▼
                                ChromaDB
                                    │
                                    ▼
                           Semantic Retrieval
                                    │
                                    ▼
                            Prompt Construction
                                    │
                                    ▼
                           Ollama (Qwen 2.5)
                                    │
                                    ▼
                                FastAPI
                                    │
                                    ▼
                               Open WebUI
```

---

# 🛠 Technologies

| Technologie | Utilisation |
|-------------|-------------|
| Python 3.13 | Backend |
| Docker | Conteneurisation |
| Docker Compose | Orchestration |
| LangChain | Framework RAG |
| Ollama | Inférence locale |
| Qwen2.5:3b | Modèle de génération |
| nomic-embed-text | Modèle d'embeddings |
| ChromaDB | Base vectorielle |
| FastAPI | API REST |
| Open WebUI | Interface conversationnelle |
| Nginx | Reverse Proxy |

---

# 📂 Structure du Projet

```text
infra-ia-souveraine/

├── Documents/
│   ├── pdf/
│   ├── word/
│   └── markdown/
│
├── RAG/
│
│   ├── api/
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── main.py
│   │   ├── rag_service.py
│   │   └── schemas.py
│   │
│   ├── chains/
│   │   └── rag_chain.py
│   │
│   ├── chunking/
│   │   └── text_chunker.py
│   │
│   ├── embeddings/
│   │   ├── embedder.py
│   │   └── vector_store.py
│   │
│   ├── generation/
│   │   └── llm.py
│   │
│   ├── ingest/
│   │   └── loader.py
│   │
│   ├── retrieval/
│   │   └── retriever.py
│   │
│   └── config.py
│
├── Tests/
│
├── docker-compose.yml
├── requirements.txt
├── requirements-api.txt
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Cloner le projet

```bash
git clone <repository-url>

cd infra-ia-souveraine
```

---

## 2️⃣ Créer un environnement virtuel

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux

```bash
source .venv/bin/activate
```

---

## 3️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
pip install -r requirements-api.txt
```

---

# 🐳 Déploiement Docker

Lancer l'infrastructure :

```bash
docker compose up -d
```

Vérifier :

```bash
docker ps
```

Services attendus :

- ollama
- chromadb
- open-webui
- nginx

---

# 🤖 Téléchargement des modèles

## Modèle LLM

```bash
docker exec -it ollama ollama pull qwen2.5:3b
```

## Modèle Embedding

```bash
docker exec -it ollama ollama pull nomic-embed-text
```

Vérification :

```bash
docker exec -it ollama ollama list
```

Résultat attendu :

```text
NAME                  SIZE

qwen2.5:3b            ~2GB
nomic-embed-text      ~274MB
```

---

# 🔥 Construction de la Base Vectorielle

## 1. Chargement documentaire

```bash
python -m Tests.test_loader
```

---

## 2. Chunking

Configuration :

```python
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
```

Exécution :

```bash
python -m Tests.test_chunker
```

---

## 3. Génération des embeddings

```bash
python -m Tests.test_embeddings_pipeline
```

Résultat attendu :

```text
Documents chargés : 12

Chunks générés : 118

Embedding model chargé : nomic-embed-text

118 chunks indexés.
```

---

# 🔎 Test du Pipeline RAG

```bash
python -m Tests.test_rag_chain
```

Exemple :

```text
Question :

Quelle est la durée du stage ?

Réponse :

Le stage se déroule du 15 juin 2026 au 14 août 2026,
soit une durée de 9 semaines.
```

---

# 🌐 API REST

Lancer :

```bash
uvicorn RAG.api.main:app --reload --port 8001
```

Swagger :

```text
http://localhost:8001/docs
```

Health Check :

```text
http://localhost:8001/health
```

---

# 🔐 Authentification

Créer un fichier :

```text
.env
```

Contenu :

```env
API_TOKEN=rayssen123
```

---

# 🔌 Endpoints Compatibles OpenAI

---

## Chat Completions

```http
POST /v1/chat/completions
```

Exemple :

```json
{
  "model": "neoledge-rag",
  "messages": [
    {
      "role": "user",
      "content": "Quelle est la durée du stage ?"
    }
  ]
}
```

---

## Embeddings

```http
POST /v1/embeddings
```

---

## Models

```http
GET /v1/models
```

---

# 🖥 Intégration Open WebUI

## URL

```text
http://host.docker.internal:8001/v1
```

## Authentification

```text
Bearer Token
```

## API Key

```text
rayssen123
```

## Modèle

```text
neoledge-rag
```

---

# 🧪 Tests Disponibles

## Chargement documentaire

```bash
python -m Tests.test_loader
```

---

## Chunking

```bash
python -m Tests.test_chunker
```

---

## Embeddings

```bash
python -m Tests.test_embeddings_pipeline
```

---

## Chaîne RAG

```bash
python -m Tests.test_rag_chain
```

---

## API

```bash
pytest Tests/test_api.py
```

Tests d'intégration :

```bash
pytest Tests/test_api.py -m integration
```

---

# 🔌 Ports Utilisés

| Service | Port |
|----------|------|
| Open WebUI | 80 |
| Ollama | 11434 |
| ChromaDB | 8000 |
| FastAPI | 8001 |

---

# 📊 État du Projet

| Module | Status |
|---------|---------|
| Infrastructure Docker | ✅ |
| Ollama | ✅ |
| Open WebUI | ✅ |
| Nginx | ✅ |
| Ingestion documentaire | ✅ |
| Chunking | ✅ |
| Embeddings | ✅ |
| ChromaDB | ✅ |
| Retrieval sémantique | ✅ |
| Chaîne RAG | ✅ |
| API FastAPI | ✅ |
| Authentification | ✅ |
| Swagger | ✅ |
| Compatibilité OpenAI | ✅ |
| Intégration OpenWebUI | ✅ |

---

# 🎯 Exemple de Pipeline

```text
Question utilisateur
        ↓
Embedding de la question
        ↓
Recherche dans ChromaDB
        ↓
Récupération des chunks pertinents
        ↓
Construction du prompt
        ↓
Qwen 2.5
        ↓
Réponse contextualisée
```

---

# 👨‍💻 Auteur

**Rayssen Draouil**

Stage Été 2026

**NeoLedge – Infrastructure IA Souveraine**
