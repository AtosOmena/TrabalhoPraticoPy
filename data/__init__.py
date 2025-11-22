
"""
Camada de Dados - Package Principal
Exporta interfaces e implementações de repositórios
"""

# Interfaces
from data.repositories.word_repository import IWordRepository
from data.repositories.player_repository import IPlayerRepository
from data.repositories.history_repository import IHistoryRepository

# Implementações
from data.storage.file_word_repository import FileWordRepository
from data.storage.file_player_repository import FilePlayerRepository
from data.storage.file_history_repository import FileHistoryRepository

__all__ = [
    'IWordRepository',
    'IPlayerRepository',
    'IHistoryRepository',
    'FileWordRepository',
    'FilePlayerRepository',
    'FileHistoryRepository',
]