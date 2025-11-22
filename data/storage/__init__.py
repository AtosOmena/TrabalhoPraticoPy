
"""
Data Storage Package
Contém implementações concretas de repositórios
"""

from data.storage.file_word_repository import FileWordRepository
from data.storage.file_player_repository import FilePlayerRepository
from data.storage.file_history_repository import FileHistoryRepository

__all__ = [
    'FileWordRepository',
    'FilePlayerRepository',
    'FileHistoryRepository',
]