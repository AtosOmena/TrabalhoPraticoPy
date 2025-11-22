"""
Use Case: ScoreboardUseCase
Gerenciar operações relacionadas ao placar
"""

from typing import List, Optional

from domain.entities.player import Player


class ScoreboardUseCase:
    """
    Caso de uso: gerenciamento do placar
    """
    
    def __init__(self, player_repository):
        """
        Args:
            player_repository: Implementação de IPlayerRepository
        """
        self.player_repository = player_repository
    
    def get_ranking(self, limit: int = 10) -> List[Player]:
        """
        Retorna ranking de jogadores ordenado por vitórias
        
        Usa list comprehension e sobrecarga de operadores (__gt__)
        da classe Player para ordenação
        
        Args:
            limit: Número máximo de jogadores a retornar
        
        Returns:
            Lista de jogadores ordenada (do melhor para o pior)
        
        Exemplo:
            top_10 = scoreboard_use_case.get_ranking(limit=10)
            for i, player in enumerate(top_10, 1):
                print(f"{i}. {player}")
        """
        all_players = self.player_repository.get_ranking()
        
        # Filtra jogadores que jogaram pelo menos uma vez
        active_players = [p for p in all_players if p.total_games > 0]
        
        return active_players[:limit]
    
    def get_top_players_by_win_rate(self, limit: int = 10, min_games: int = 5) -> List[Player]:
        """
        Retorna jogadores com melhor taxa de vitória
        
        Args:
            limit: Número máximo de jogadores
            min_games: Mínimo de jogos para ser considerado
        
        Returns:
            Lista de jogadores ordenada por win_rate
        """
        all_players = self.player_repository.get_all()
        
        # Filtra jogadores com número mínimo de jogos
        qualified_players = [
            player for player in all_players 
            if player.total_games >= min_games
        ]
        
        # Ordena por win_rate (decrescente)
        sorted_by_wr = sorted(
            qualified_players,
            key=lambda p: p.win_rate,
            reverse=True
        )
        
        return sorted_by_wr[:limit]
    
    def get_player_rank(self, player_name: str) -> Optional[int]:
        """
        Retorna a posição do jogador no ranking
        
        Args:
            player_name: Nome do jogador
        
        Returns:
            Posição no ranking (1-indexed), ou None se não encontrado
        """
        ranking = self.get_ranking(limit=1000)  # Pega todos
        
        for index, player in enumerate(ranking, start=1):
            if player.name.lower() == player_name.lower():
                return index
        
        return None

    def get_total_players(self) -> int:
        """Retorna número total de jogadores cadastrados"""
        all_players = self.player_repository.get_all()
        return len(all_players)
    
    def get_active_players_count(self) -> int:
        """Retorna número de jogadores que já jogaram pelo menos uma vez"""
        all_players = self.player_repository.get_all()
        
        active = [p for p in all_players if p.total_games > 0]
        
        return len(active)
    
    def get_best_player(self) -> Optional[Player]:
        """
        Retorna o melhor jogador (mais vitórias)
        
        Returns:
            Player com mais vitórias, ou None se não houver jogadores
        """
        ranking = self.get_ranking(limit=1)
        
        return ranking[0] if ranking else None
