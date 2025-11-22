"""
Interface: IHistoryRepository
Definir contrato para repositório de histórico
"""

from abc import ABC, abstractmethod
from typing import List

from domain.entities.game_history import GameHistory


class IHistoryRepository(ABC):
    """
    Interface para repositório de histórico
    Define operações para gerenciar registros de partidas
    """
    
    @abstractmethod
    def get_all(self) -> List[GameHistory]:
        """
        Retorna todo o histórico de partidas
        
        Returns:
            Lista de objetos GameHistory
        """
        pass
    
    @abstractmethod
    def save(self, history: GameHistory) -> bool:
        """
        Salva um registro de partida no histórico
        Sempre adiciona novo registro (append-only)
        
        Args:
            history: Objeto GameHistory a ser salvo
        
        Returns:
            True se salvo com sucesso, False caso contrário
        """
        pass
