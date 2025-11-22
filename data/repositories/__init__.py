
"""
Data Repositories Package
Contém as interfaces (contratos) de repositórios
"""

from data.repositories.word_repository import IWordRepository
from data.repositories.player_repository import IPlayerRepository
from data.repositories.history_repository import IHistoryRepository

__all__ = [
    'IWordRepository',
    'IPlayerRepository',
    'IHistoryRepository',
]