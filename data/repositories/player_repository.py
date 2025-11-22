"""
Interface: IPlayerRepository
Definir contrato para repositório de jogadores
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.player import Player


class IPlayerRepository(ABC):
    """
    Interface para repositório de jogadores
    Define operações CRUD para gerenciar jogadores
    """
    
    @abstractmethod
    def get_all(self) -> List[Player]:
        """
        Retorna todos os jogadores
        
        Returns:
            Lista de objetos Player
        """
        pass
    
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Player]:
        """
        Busca jogador por nome (case-insensitive)
        
        Args:
            name: Nome do jogador
        
        Returns:
            Objeto Player se encontrado, None caso contrário
        """
        pass
    
    @abstractmethod
    def save(self, player: Player) -> bool:
        """
        Salva ou atualiza um jogador
        Se o jogador já existe (mesmo nome), atualiza
        Caso contrário, cria novo registro
        
        Args:
            player: Objeto Player a ser salvo
        
        Returns:
            True se salvo com sucesso, False caso contrário
        """
        pass
    
    @abstractmethod
    def save_game_result(self, player_name: str, won: bool) -> bool:
        """
        Salva resultado de uma partida para um jogador
        
        Args:
            player_name: Nome do jogador
            won: True se venceu, False se perdeu
        
        Returns:
            True se salvo com sucesso, False caso contrário
        """
        pass
    
    @abstractmethod
    def get_ranking(self, limit: Optional[int] = None) -> List[Player]:
        """
        Retorna jogadores ordenados por vitórias (ranking)
        
        Args:
            limit: Número máximo de jogadores a retornar (None = todos)
        
        Returns:
            Lista de Players ordenada por vitórias (decrescente)
        """
        pass
