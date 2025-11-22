
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from .game_state import GameState

@dataclass
class GameHistory:
    """Representa um registro de partida no histórico"""
    
    date: str
    player_name: str
    word: str
    result: str
    attempts_used: int
    duration_seconds: int
    timestamp: datetime = field(default_factory=datetime.now)
    
    @classmethod
    def from_game_state(cls, game_state: GameState) -> 'GameHistory':
        """Factory method: cria histórico a partir do estado do jogo"""
        return cls(
            date=game_state.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            player_name=game_state.player_name,
            word=game_state.word,
            result='WIN' if game_state.is_won else 'LOSS',
            attempts_used=game_state.wrong_attempts,
            duration_seconds=game_state.duration_seconds,
            timestamp=game_state.start_time
        )
    
    def to_file_format(self) -> str:
        """Converte para formato de arquivo (CSV-like)"""
        return f"{self.date}|{self.player_name}|{self.word}|{self.result}|{self.attempts_used}|{self.duration_seconds}"
    
    @classmethod
    def from_file_format(cls, line: str) -> 'GameHistory':
        """Cria objeto a partir de uma linha do arquivo"""
        parts = line.strip().split('|')
        if len(parts) != 6:
            raise ValueError(f"Formato inválido: {line}")
        
        return cls(
            date=parts[0],
            player_name=parts[1],
            word=parts[2],
            result=parts[3],
            attempts_used=int(parts[4]),
            duration_seconds=int(parts[5])
        )
    
    # Métodos Mágicos
    def __str__(self) -> str:
        result_emoji = "✓" if self.result == 'WIN' else "✗"
        return (f"{result_emoji} {self.date} | {self.player_name} | "
                f"Palavra: {self.word} | Tentativas: {self.attempts_used}")
    
    def __repr__(self) -> str:
        return f"GameHistory(player='{self.player_name}', word='{self.word}', result='{self.result}')"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GameHistory):
            return False
        return (self.player_name == other.player_name and 
                self.word == other.word and 
                self.date == other.date)
    
    def __add__(self, other: 'GameHistory') -> List['GameHistory']:
        """Combina dois históricos em uma lista"""
        return [self, other]
