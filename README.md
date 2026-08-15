# Neo-stage-llm-2026

# Infrastructure IA Souveraine – NeoLedge

## Description

Ce projet met en place une **infrastructure IA locale et souveraine** basée sur un modèle LLM Open Source et un pipeline **RAG (Retrieval-Augmented Generation)**.

L'objectif est de permettre à un assistant conversationnel de répondre aux questions des utilisateurs en s'appuyant sur la documentation interne de NeoLedge, tout en conservant les données et les traitements dans une infrastructure locale.

Le projet repose principalement sur des composants Open Source exécutés localement :

* Ollama
* Qwen
* nomic-embed-text
* ChromaDB
* LangChain
* FastAPI
* Open WebUI
* Nginx
* Prometheus
* Grafana
* Docker / Docker Compose

---

# Architecture

```text
                         DOCUMENTATION INTERNE
                    PDF / Word / Markdown
                              │
                              ▼
                 ┌─────────────────────────┐
                 │    Document Loaders     │
                 │ PDF / Word / Markdown   │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │       Chunking          │
                 │ RecursiveCharacter      │
                 │ TextSplitter            │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │       Embeddings        │
                 │    nomic-embed-text     │
                 │         Ollama          │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │       ChromaDB          │
                 │     Vector Store        │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │   Semantic Retrieval    │
                 │       LangChain         │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │         Qwen            │
                 │       Ollama LLM        │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │        FastAPI          │
                 │      REST API           │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │       Open WebUI         │
                 │ Conversation Interface   │
                 └─────────────────────────┘


                    MONITORING & OBSERVABILITY

                 FastAPI /metrics
                         │
                         ▼
                 ┌───────────────┐
                 │   Prometheus  │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │    Grafana    │
                 │   Dashboard   │
                 └───────────────┘
```

---

# Technologies

| Technologie      | Rôle                                  |
| ---------------- | ------------------------------------- |
| Python 3.13      | Développement backend et pipeline RAG |
| Ollama           | Exécution locale des modèles          |
| Qwen 2.5         | Modèle LLM pour la génération         |
| nomic-embed-text | Génération des embeddings             |
| LangChain        | Orchestration du pipeline RAG         |
| ChromaDB         | Base vectorielle                      |
| FastAPI          | API REST                              |
| Open WebUI       | Interface conversationnelle           |
| Nginx            | Reverse proxy                         |
| Prometheus       | Collecte des métriques                |
| Grafana          | Visualisation et monitoring           |
| Docker           | Conteneurisation                      |
| Docker Compose   | Orchestration des services            |

---

# Prérequis

Installer :

* Docker Desktop
* Python 3.13+
* Git

---

# Cloner le projet

```bash
git clone <repository-url>

cd infra-ia-souveraine
```

---

# Créer l'environnement Python

Sous Windows :

```bash
python -m venv .venv
```

Activer l'environnement :

```bash
.venv\Scripts\activate
```

---

# Installer les dépendances

```bash
pip install -r requirements.txt
```

---

# Démarrer l'infrastructure

Lancer Docker Desktop puis :

```bash
docker compose up -d
```

Vérifier les conteneurs :

```bash
docker ps
```

Les principaux services sont :

* `ollama`
* `open-webui`
* `chromadb`
* `nginx`
* `prometheus`
* `grafana`

---

# Télécharger les modèles Ollama

## Qwen

```bash
docker exec -it ollama ollama pull qwen2.5-coder:1.5b
```

## Embeddings

```bash
docker exec -it ollama ollama pull nomic-embed-text
```

Vérifier les modèles installés :

```bash
docker exec -it ollama ollama list
```

---

# Accéder aux services

## Open WebUI

```text
http://localhost
```

## FastAPI

```text
http://localhost:8001
```

## Documentation Swagger

```text
http://localhost:8001/docs
```

## Prometheus

```text
http://localhost:9090
```

## Grafana

```text
http://localhost:3000
```

---

# Structure du projet

```text
infra-ia-souveraine/

│
├── Documents/
│   ├── pdf/
│   ├── word/
│   └── markdown/
│
├── RAG/
│   ├── ingest/
│   ├── chunking/
│   ├── embeddings/
│   ├── retrieval/
│   └── config.py
│
├── Tests/
│   ├── test_loader.py
│   ├── test_chunker.py
│   ├── test_embeddings_pipeline.py
│   ├── test_rag_chain.py
│   ├── test_api.py
│   └── test_rag_evaluation.py
│
├── docker-compose.yml
├── Dockerfile.api
├── requirements.txt
└── README.md
```

---

# Pipeline RAG

Le pipeline RAG est composé de plusieurs étapes.

## 1. Ingestion documentaire

Le système charge automatiquement les documents internes au format :

* PDF
* Word
* Markdown

Commande :

```bash
python -m Tests.test_loader
```

---

## 2. Chunking

Les documents sont découpés en morceaux afin de permettre une recherche sémantique efficace.

Configuration actuelle :

```text
Chunk Size    = 500
Chunk Overlap = 100
```

Commande :

```bash
python -m Tests.test_chunker
```

---

## 3. Embeddings

Chaque chunk est transformé en vecteur avec :

```text
nomic-embed-text
```

Les embeddings sont ensuite indexés dans :

```text
ChromaDB
```

Commande :

```bash
python -m Tests.test_embeddings_pipeline
```

---

## 4. Retrieval

Lorsqu'une question est posée, le système recherche les chunks les plus pertinents dans ChromaDB à l'aide d'une recherche sémantique.

Le retriever transmet ensuite les documents pertinents au LLM.

---

## 5. Génération

Le contexte récupéré est transmis au modèle Qwen exécuté localement avec Ollama.

Le LLM génère ensuite une réponse basée sur les informations récupérées.

---

# API REST FastAPI

Une API REST a été développée afin d'exposer le pipeline RAG.

L'API permet notamment de :

* recevoir une requête utilisateur ;
* effectuer le retrieval ;
* construire le contexte ;
* appeler le LLM ;
* retourner la réponse ;
* exposer les métriques Prometheus.

Documentation interactive :

```text
http://localhost:8001/docs
```

---

# Configuration

Les paramètres principaux sont définis dans :

```text
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

# Monitoring & Observability

Le pipeline RAG est instrumenté avec **Prometheus** afin de suivre ses performances et son état d'exécution.

Les métriques sont exposées par l'API :

```text
http://localhost:8001/metrics
```

Prometheus collecte automatiquement ces métriques.

## Métriques principales

```text
rag_requests_total
```

Nombre total de requêtes RAG réussies.

```text
rag_errors_total
```

Nombre total de requêtes RAG en erreur.

```text
rag_retrieval_duration_seconds
```

Durée du retrieval.

```text
rag_llm_duration_seconds
```

Durée de génération du LLM.

```text
rag_total_duration_seconds
```

Durée totale du pipeline RAG.

```text
rag_retrieved_documents
```

Nombre de documents/chunks récupérés lors de la dernière exécution.

---

# Correction de la collecte des métriques

Une attention particulière a été portée à la cohérence des métriques.

Initialement, certaines métriques pouvaient être enregistrées pendant l'exécution du pipeline, avant que celui-ci soit complètement terminé.

Cela pouvait produire des statistiques incohérentes lorsqu'une exécution était interrompue entre le retrieval et la génération LLM.

La collecte a donc été déplacée dans un **bloc de succès unique**.

Ainsi :

* une exécution RAG réussie incrémente `rag_requests_total` une seule fois ;
* une exécution réussie produit une observation dans les trois histogrammes de durée ;
* une exécution en échec incrémente uniquement `rag_errors_total`.

Cette approche garantit une meilleure cohérence entre les différentes métriques.

---

# Grafana

Grafana est utilisé pour visualiser les métriques collectées par Prometheus.

Le dashboard permet notamment de suivre :

* Total RAG Requests
* RAG Errors
* Retrieval Duration
* LLM Generation Duration
* Total RAG Duration
* Retrieved Documents

Architecture :

```text
FastAPI
   │
   │ /metrics
   ▼
Prometheus
   │
   ▼
Grafana
   │
   ▼
RAG Monitoring Dashboard
```

La cible `rag-api` est également surveillée par Prometheus afin de vérifier que l'API est accessible.

---

# Évaluation automatique du RAG

Une suite de tests dédiée à l'évaluation du pipeline RAG a été mise en place.

Le test permet de vérifier :

* la pertinence des réponses ;
* la récupération des documents attendus ;
* la capacité du système à répondre à partir des documents internes ;
* le comportement du pipeline sur différents types de questions.

L'évaluation utilise un ensemble de questions avec :

```text
Question
Réponse attendue
Réponse obtenue
Sources attendues
Sources obtenues
```

Lancement :

```bash
pytest Tests/test_rag_evaluation.py -s
```

Le jeu d'évaluation contient actuellement **10 cas de test**.

Exemple :

```text
Question :
Quelle est la durée du stage ?

Réponse attendue :
9 semaines.

Réponse obtenue :
La durée du stage est de 9 semaines,
allant du 15/06/2026 au 14/08/2026.
```

Le vector store utilisé pour l'évaluation contient actuellement :

```text
118 chunks
```

---

# Tests

## Test du chargement documentaire

```bash
python -m Tests.test_loader
```

## Test du chunking

```bash
python -m Tests.test_chunker
```

## Test des embeddings

```bash
python -m Tests.test_embeddings_pipeline
```

## Test de la chaîne RAG

```bash
python -m Tests.test_rag_chain
```

## Test de l'API

```bash
python -m Tests.test_api
```

## Évaluation automatique du RAG

```bash
pytest Tests/test_rag_evaluation.py -s
```

---

# Vérification des services

## Ollama

```bash
docker ps
```

Tester l'API :

```bash
curl http://localhost:11434/api/tags
```

## ChromaDB

```bash
curl http://localhost:8000/api/v2/heartbeat
```

## FastAPI

```bash
curl http://localhost:8001/metrics
```

## Prometheus

```text
http://localhost:9090/targets
```

La cible `rag-api` doit apparaître avec l'état :

```text
UP
```

---

# Ports utilisés

| Service            |  Port |
| ------------------ | ----: |
| Nginx / Open WebUI |    80 |
| FastAPI            |  8001 |
| Ollama             | 11434 |
| ChromaDB           |  8000 |
| Prometheus         |  9090 |
| Grafana            |  3000 |

---

# État actuel du projet

* ✔ Infrastructure Docker / Docker Compose
* ✔ Ollama
* ✔ Qwen 2.5
* ✔ Open WebUI
* ✔ Nginx
* ✔ ChromaDB
* ✔ Ingestion PDF / Word / Markdown
* ✔ Chunking
* ✔ Embeddings `nomic-embed-text`
* ✔ Indexation vectorielle
* ✔ Retrieval sémantique
* ✔ Chaîne RAG
* ✔ API REST FastAPI
* ✔ Documentation Swagger
* ✔ Intégration avec l'interface conversationnelle
* ✔ Monitoring Prometheus
* ✔ Dashboard Grafana
* ✔ Métriques RAG
* ✔ Évaluation automatique du pipeline RAG
* ✔ Tests automatisés

---

# Objectifs réalisés

L'infrastructure permet désormais de disposer d'un assistant IA local capable de :

1. charger des documents internes ;
2. les découper en chunks ;
3. générer leurs embeddings localement ;
4. les indexer dans ChromaDB ;
5. effectuer une recherche sémantique ;
6. transmettre le contexte pertinent au LLM ;
7. générer une réponse avec Qwen ;
8. exposer le pipeline via une API FastAPI ;
9. superviser les performances avec Prometheus ;
10. visualiser les métriques avec Grafana ;
11. évaluer automatiquement la qualité du pipeline RAG.

L'ensemble est conteneurisé et peut être déployé localement avec Docker Compose.

---

# Souveraineté et confidentialité

L'objectif principal de cette infrastructure est de limiter la dépendance aux services IA propriétaires et de conserver les traitements au sein de l'environnement local.

Les composants principaux du pipeline — LLM, embeddings, vector store, API et monitoring — sont exécutés localement.

Cette architecture permet notamment de mieux maîtriser :

* les données utilisées par le RAG ;
* les documents internes ;
* les modèles utilisés ;
* l'infrastructure d'exécution ;
* les performances du système ;
* la supervision du pipeline.

---

# Auteur

**Rayssen Draouil**

Stage Été 2026

**NeoLedge – Infrastructure IA Souveraine**
