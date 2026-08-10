"""Configuration pytest partagée.

Ajoute la racine du dépôt au chemin d'import pour garantir que les modules
RAG restent importables pendant la collecte des tests.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))