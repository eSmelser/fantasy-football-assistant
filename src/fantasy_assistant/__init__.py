"""
Fantasy Football Draft Assistant

A professional-grade fantasy football draft helper with AI-powered recommendations,
real-time draft tracking, and comprehensive strategy integration.

Author: Evan Smelser
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Evan Smelser"
__email__ = "your.email@example.com"

from .models.database import DatabaseManager
from .models.player import Player
from .services.draft_engine import DraftEngine
from .services.ai_recommender import AIRecommender

__all__ = [
    "DatabaseManager",
    "Player", 
    "DraftEngine",
    "AIRecommender",
]