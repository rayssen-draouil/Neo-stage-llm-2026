## **STAGE ETE - 2026** 

**Déploiement d'un LLM Open Source en Entreprise** 

Référence : **#NEO-STAGE-ETE-2026-01** Durée : du 15/06/2026 au 14/08/2026 Type : Stage d’été (ingénieur / mastère) Nombre de stagiaires : 2 (Minimum) 

Copyright : © 2026 - NeoLedge 

STATION NEOLEDGE, Zarzis Smart Center, Parc des Activités Économiques – 4137 Zarzis – Tunisie, www.neoledge.com MF : 1684439M au capital de 10 000 EUROS 

NEO-STAGE-ETE-2026-01 

## **1 Contexte et problématique** ~~SE —~~ 

NeoLedge est un éditeur de solutions ECM (Enterprise Content Management) en mode SaaS, spécialisé dans la dématérialisation de documents, la gestion électronique de documents (GED) et la capture omnicanale de l'information. Ses équipes techniques produisent et consomment quotidiennement une grande quantité de documentation interne : spécifications fonctionnelles, guides d'intégration, bases de connaissances, tickets, comptes-rendus, etc. 

L'essor des Grands Modèles de Langage (LLM) transforme profondément les pratiques de développement logiciel et de gestion de la connaissance en entreprise. Les solutions propriétaires comme GPT-4 ou Claude, si elles sont performantes, imposent des contraintes significatives : coût à l'usage, envoi de données potentiellement sensibles vers des serveurs externes, dépendance à des fournisseurs tiers, et impossibilité de garantir la confidentialité des informations métier. 

Les LLMs open source — Mistral, LLaMA, Qwen, Gemma — offrent aujourd'hui une alternative crédible et maîtrisable. Combinés à des outils de déploiement local comme Ollama, ils permettent de construire une infrastructure IA souveraine, hébergée entièrement en interne, sans exposer les données de l'entreprise. Couplés à une approche RAG (Retrieval-Augmented Generation), ils peuvent interroger intelligemment la documentation interne et augmenter la productivité des équipes. 

Ce stage s'inscrit dans une démarche d'innovation interne visant à concevoir, déployer et documenter une telle infrastructure IA, reproductible et opérationnelle pour les équipes techniques de NeoLedge. 

© NeoLedge, 2026                                                                                                                                 2/10 

NEO-STAGE-ETE-2026-01 

## **2 Résumé** ~~SE~~ 

Ce stage vise à déployer un LLM open source en local (Mistral, LLaMA, Qwen…) avec une interface web utilisateur accessible à l'équipe. Le stagiaire commencera par une étude comparative des modèles disponibles, puis mettra en place un pipeline RAG permettant d'interroger les documents internes de l'entreprise avec une précision contextuelle. Le modèle sera ensuite exposé via une API REST standardisée, compatible avec le format OpenAI, authentifiée et documentée. L'ensemble de la solution sera conteneurisé sous Docker et documenté pour être entièrement reproductible. En objectif bonus, le stagiaire implémentera un serveur MCP connecté à VS Code pour créer un agent de développement IA souverain, sans dépendance à des outils propriétaires. 

© NeoLedge, 2026                                                                                                                                 3/10 

NEO-STAGE-ETE-2026-01 

## **3 Description détaillée** ~~SE —~~ 

## **1. Étude comparative des LLMs open source** 

La première étape consiste à analyser et comparer de manière rigoureuse les principaux modèles open source disponibles : Mistral, LLaMA 3, Qwen2.5-Coder, Gemma 2. La comparaison portera sur les critères suivants : performances sur des benchmarks standards (MMLU, HumanEval), licences d'utilisation commerciale, contraintes matérielles (RAM, GPU), capacités multilingues (arabe, français, anglais), et latence d'inférence sur le matériel disponible. Cette analyse débouchera sur un rapport de recommandation motivé du modèle retenu. 

## **2. Déploiement local avec interface web** 

La solution reposera sur Ollama comme moteur d'inférence local, permettant de charger et servir le modèle sélectionné. Open WebUI sera déployé comme interface conversationnelle accessible depuis un navigateur. Un reverse proxy Nginx assurera la gestion des accès. L'ensemble sera orchestré via Docker Compose pour garantir la portabilité et la reproductibilité du déploiement. 

## **3. Pipeline RAG sur documents internes** 

Un pipeline RAG (Retrieval-Augmented Generation) sera mis en place pour permettre au LLM d'interroger la documentation interne de NeoLedge. Le pipeline comprendra : 

- Ingestion des documents sources (PDF, Word, Markdown) avec extraction et découpage en chunks ; 

- Génération des embeddings via un modèle d'encodage local (nomic-embed-text ou équivalent) ; 

- Indexation dans une base vectorielle (ChromaDB ou Qdrant) ; 

- Requêtage sémantique : à chaque question, les passages les plus pertinents sont récupérés et injectés dans le contexte du LLM pour enrichir ses réponses avec la connaissance documentaire de l'entreprise. 

© NeoLedge, 2026                                                                                                                                 4/10 

NEO-STAGE-ETE-2026-01 

## **4. API REST standardisée** 

Une API FastAPI sera développée pour exposer les capacités du LLM de manière standardisée, compatible avec le format OpenAI (endpoints /v1/chat/completions, /v1/embeddings). L'API inclura une authentification par token, une documentation Swagger auto-générée, et des tests d'intégration. Elle sera conteneurisée dans un Dockerfile dédié, indépendant du reste de l'infrastructure. 

## **5. Serveur MCP et agent VS Code (objectif bonus)** 

Un serveur MCP (Model Context Protocol) sera implémenté pour exposer des outils au LLM : lecture de fichiers du projet, exécution de commandes, recherche sémantique dans le codebase. Ce serveur sera connecté à VS Code, transformant le LLM local en un agent de développement souverain capable d'assister les développeurs en complétion de code, génération de tests unitaires et revue de code — sans aucune dépendance à des services propriétaires. 

## **6. Objectifs** 

## **a. Objectifs principaux** 

- Évaluer et comparer les principaux LLMs open source selon des critères techniques objectifs (performance, licence, contraintes matérielles, capacités multilingues). 

- Déployer un LLM en local avec une interface web accessible et utilisable par l'équipe. 

- Mettre en place un pipeline RAG exploitant les documents internes de l'entreprise. 

- Exposer le modèle via une API REST standardisée, compatible OpenAI, authentifiée, documentée et testée. 

- Conteneuriser l'ensemble de la solution via Docker Compose et produire une documentation technique complète et reproductible. 

## **b. Objectif bonus** 

- Implémenter un serveur MCP connecté à VS Code pour créer un agent de développement IA local et souverain, sans dépendance à des outils propriétaires (Copilot, ChatGPT, etc.). 

© NeoLedge, 2026                                                                                                                                 5/10 

NEO-STAGE-ETE-2026-01 

## **7. Compétences requises** 

|**Domaine**|**Niveau attendu**|
|---|---|
|Python|Maîtrise (indispensable)|
|**API REST / FastAPI**|Notions de base (endpoints, authentification)|
|Docker / Docker Compose|Notions de base (conteneurisation, orchestration)|
|Linux / ligne de commande|Maîtrise de base|
|NLP / LLM|Notions générales (inférence, embeddings, RAG)|
|Git / versioning|Maîtrise de base|



## **8. Compétences développées** 

Au terme de ce stage, le stagiaire aura acquis une expertise concrète dans les domaines suivants : 

## **Compétences techniques** 

- Compréhension approfondie des LLMs open source et de leurs conditions de déploiement en environnement contraint (on-premise, GPU limité). 

- Maîtrise pratique de la chaîne RAG complète : ingestion documentaire, vectorisation, indexation sémantique et génération augmentée. 

- Conception et développement d'une API REST professionnelle (FastAPI, authentification, Swagger, tests d'intégration). 

- Maîtrise de la conteneurisation avec Docker et Docker Compose dans un contexte d'infrastructure IA multi-services. 

- Sensibilisation aux enjeux de souveraineté numérique, de confidentialité des données et d'IA responsable en entreprise. 

## **Compétences méthodologiques et organisationnelles** 

- **Travail en méthode SCRUM :** le stage est organisé en sprints de deux semaines, avec des cérémonies agiles (planification de sprint, revue de fin de sprint, rétrospective). Le stagiaire sera initié aux pratiques d'une équipe de développement moderne et apprendra à estimer, prioriser et livrer des incréments fonctionnels à chaque itération. 

© NeoLedge, 2026                                                                                                                                 6/10 

NEO-STAGE-ETE-2026-01 

- **Utilisation d'outils de gestion de tâches :** découpage du Backlog en tâches unitaires, suivi de l'avancement via un outil dédié (Jira, Trello ou équivalent), mise à jour régulière des statuts et respect des critères d'acceptation définis en début de sprint. Le stagiaire développera une rigueur de planification directement transposable à un environnement professionnel ou à un projet de fin d'études. 

- **Collaboration et travail en équipe :** le stagiaire s'intégrera dans une équipe d'ingénieurs, participera aux échanges techniques, soumettra son code en revue ( _pull requests_ ), et apprendra à donner et recevoir des retours constructifs dans un cadre professionnel. La nature transversale du sujet — à l'intersection du DevOps, du NLP et du développement backend — favorise naturellement les interactions avec des profils complémentaires. 

- **Communication et restitution du travail :** à chaque fin de sprint, le stagiaire présentera son avancement à l'équipe encadrante sous forme de démonstration technique et de synthèse orale. Cette pratique régulière développe la capacité à vulgariser des choix d'architecture, à argumenter ses décisions techniques, et à structurer une présentation claire et convaincante — une compétence directement réutilisable lors de la soutenance de projet de fin d'études. 

## **9. Stack technologique** 

|**Catégorie**|**Outils / Technologies**|
|---|---|
|Langage principal|Python 3.10+|
|Moteur d'inférence LLM|Ollama|
|Modèles LLM|Mistral, LLaMA 3, Qwen2.5-Coder, Gemma 2|
|Interface web|Open WebUI|
|Framework API|FastAPI|
|Pipeline RAG|LangChain ou LlamaIndex|
|Modèle d'embeddings|nomic-embed-text (via Ollama)|
|Base vectorielle|ChromaDB ou Qdrant|
|Reverse proxy|Nginx|
|Conteneurisation|Docker, Docker Compose|
|Protocole agent (bonus)|Nginx|



© NeoLedge, 2026                                                                                                                                 7/10 

NEO-STAGE-ETE-2026-01 

|IDE / intégration|VS Code|
|---|---|
|Gestion de projet|Jira / Trello, Git, GitHub|



## **10. Livrables attendus** 

1. Rapport comparatif des LLMs open source évalués, avec recommandation motivée du modèle retenu. 

2. Infrastructure déployée : Ollama + Open WebUI + Nginx, orchestrée via Docker Compose, opérationnelle et accessible. 

3. Pipeline RAG fonctionnel : ingestion, vectorisation, indexation et requêtage sémantique sur le corpus documentaire NeoLedge. 

4. API REST FastAPI documentée (Swagger), authentifiée, testée et conteneurisée. 

5. Documentation technique complète : guide d'installation, guide d'utilisation, architecture de la solution. 

6. Rapport de stage technique complet (introduction, état de l'art, architecture, résultats, conclusion). 

7. Présentation finale (soutenance interne, ~20 min + questions). 

8. Dépôt Git propre avec README, instructions d'installation et exemples d'utilisation. 

## **11. Planning prévisionnel** 

**Période :** 15 juin 2026 → 14 août 2026 (9 semaines) 

**Rythme :** 1 sprint = 2 semaines | livrable technique à chaque fin de sprint 

|**Phase**|**Semaines**|**Semaines**<br>**Période**|**Thème**|**Livrable**|
|---|---|---|---|---|
|Démarrage|S1|15 – 21|15 – 21<br>Onboarding & montée|Onboarding & montée<br>Fiche de prise en main + rapport|
|||juin|en compétences|comparatif des LLMs|



© NeoLedge, 2026                                                                                                                                 8/10 

NEO-STAGE-ETE-2026-01 

|Sprint 1|S2 – S3|22 juin – 5|22 juin – 5|22 juin – 5|22 juin – 5<br>Déploiement local LLM|22 juin – 5<br>Déploiement local LLM|Déploiement local LLM<br>Infrastructure<br>Ollama|Ollama<br>+<br>Open|Ollama<br>+<br>Open|
|---|---|---|---|---|---|---|---|---|---|
|||juil.|juil.||+ interface web||WebUI + Nginx opérationnelle via||WebUI + Nginx opérationnelle via|
||||||||Docker Compose|||
|Sprint 2|S4 – S5|6 – 19 juil.|6 – 19 juil.||6 – 19 juil.<br>Pipeline<br>RAG|sur|sur<br>Pipeline RAG fonctionnel : ingestion,|||
||||||documents internes|documents internes|vectorisation,<br>indexation||et|
||||||||requêtage démontré|||
|Sprint 3|S6 – S7|20 juil. – 2||20 juil. – 2|20 juil. – 2<br>API REST standardisée||API FastAPI déployée, documentée|API FastAPI déployée, documentée||
|||août|||||(Swagger), authentifiée et testée|(Swagger), authentifiée et testée|(Swagger), authentifiée et testée|
|Clôture|S8 – S9|3|–|14|14<br>Tests, déploiement &|Tests, déploiement &|Tests, déploiement &<br>Solution<br>complète|déployable||
|||août|||rapport||(Docker<br>Compose)||+|
||||||||documentation<br>+|rapport|+|
||||||||présentation|||



## **Détails par sprint :** 

## **Semaine 1 — Onboarding (15 – 21 juin)** 

Découverte des produits NeoLedge (Elise, GED, workflows), prise en main de l'environnement de développement, installation des outils (Docker, Python, VS Code, Ollama). Étude comparative des LLMs open source disponibles (Mistral, LLaMA 3, Qwen2.5-Coder, Gemma 2) selon les critères de performance, licence, contraintes matérielles et capacités multilingues. 

## **Sprint 1 — Déploiement local LLM + interface web (22 juin – 5 juillet)** 

Installation et configuration d'Ollama avec le modèle retenu. Déploiement d'Open WebUI comme interface conversationnelle. Configuration du reverse proxy Nginx. Orchestration complète via Docker Compose. Validation de l'accessibilité de l'interface par l'équipe et premiers tests de génération. 

## **Sprint 2 — Pipeline RAG sur documents internes (6 – 19 juillet)** 

Mise en place du pipeline RAG complet : collecte et préparation du corpus documentaire NeoLedge (PDF, Word, Markdown), découpage en chunks, génération des embeddings avec nomic-embed-text, indexation dans ChromaDB ou Qdrant, et intégration du requêtage sémantique dans l'interface de chat. Démonstration sur des questions réelles liées à la documentation interne. 

## **Sprint 3 — API REST standardisée (20 juillet – 2 août)** 

Développement de l'API FastAPI exposant les endpoints /v1/chat/completions et /v1/embeddings au format OpenAI. Mise en place de l'authentification par token. Génération de la documentation Swagger. Écriture des tests d'intégration. Conteneurisation de l'API dans un Dockerfile dédié. Exploration de l'objectif bonus (serveur MCP + VS Code) si le temps le permet. 

© NeoLedge, 2026                                                                                                                                 9/10 

NEO-STAGE-ETE-2026-01 

## **Semaines 8 – 9 — Clôture (3 – 14 août)** 

Tests de robustesse et de charge de l'infrastructure complète. Finalisation de la documentation technique (guide d'installation, guide d'utilisation, schéma d'architecture). Rédaction du rapport de stage et préparation de la soutenance finale. 

© NeoLedge, 2026                                                                                                                                 10/10 

