
"""
Domain Use Cases Package
Contém todos os casos de uso (lógica de aplicação)
"""

from domain.use_cases.hangman_game_use_case import HangmanGameUseCase
from domain.use_cases.scoreboard_use_case import ScoreboardUseCase
from domain.use_cases.history_use_case import HistoryUseCase

__all__ = [
    'HangmanGameUseCase',
    'ScoreboardUseCase',
    'HistoryUseCase',
]