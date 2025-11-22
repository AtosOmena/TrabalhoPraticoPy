
"""
Camada de Domínio - Package Principal
Exporta todas as entidades e use cases
"""

# Exporta entidades
from domain.entities.player import Player
from domain.entities.game_state import GameState
from domain.entities.game_history import GameHistory
from domain.entities.game_mode import GameMode

# Exporta use cases
from domain.use_cases.hangman_game_use_case import HangmanGameUseCase
from domain.use_cases.scoreboard_use_case import ScoreboardUseCase
from domain.use_cases.history_use_case import HistoryUseCase

__all__ = [
    'Player',
    'GameState',
    'GameHistory',
    'GameMode',
    'HangmanGameUseCase',
    'ScoreboardUseCase',
    'HistoryUseCase',
]