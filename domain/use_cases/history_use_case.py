"""
Use Case: HistoryUseCase
Gerenciar operações relacionadas ao histórico
"""

from typing import List, Dict, Any

from domain.entities.game_history import GameHistory


class HistoryUseCase:
    """
    Caso de uso: gerenciamento do histórico
    """
    
    def __init__(self, history_repository):
        """
        Args:
            history_repository: Implementação de IHistoryRepository
        """
        self.history_repository = history_repository
    

    
    def get_recent_games(self, limit: int = 20) -> List[GameHistory]:
        """
        Retorna os jogos mais recentes
        
        Usa list comprehension para processar dados
        
        Args:
            limit: Número máximo de jogos a retornar
        
        Returns:
            Lista de GameHistory ordenada por data (mais recente primeiro)
        
        Exemplo:
            recent = history_use_case.get_recent_games(limit=10)
            for game in recent:
                print(game)
        """
        all_history = self.history_repository.get_all()
        
        # Ordena por data usando list comprehension
        sorted_history = sorted(
            all_history, 
            key=lambda h: h.timestamp if hasattr(h, 'timestamp') else h.date,
            reverse=True
        )
        
        return sorted_history[:limit]
    
    def get_player_history(self, player_name: str, limit: int = 10) -> List[GameHistory]:
        """
        Retorna histórico de um jogador específico
        
        Args:
            player_name: Nome do jogador
            limit: Número máximo de jogos
        
        Returns:
            Lista de GameHistory do jogador, ordenada por data
        
        Exemplo:
            alice_games = history_use_case.get_player_history("Alice", limit=5)
        """
        all_history = self.history_repository.get_all()
        
        # Filtra jogos do jogador
        player_games = [
            game for game in all_history 
            if game.player_name.lower() == player_name.lower()
        ]
        
        # Ordena por data
        sorted_games = sorted(
            player_games,
            key=lambda h: h.timestamp if hasattr(h, 'timestamp') else h.date,
            reverse=True
        )
        
        return sorted_games[:limit]
    
    def get_victories(self, player_name: str = None) -> List[GameHistory]:
        """
        Retorna todas as vitórias (opcionalmente de um jogador)
        
        Args:
            player_name: Nome do jogador (None = todos)
        
        Returns:
            Lista de vitórias
        """
        all_history = self.history_repository.get_all()
        
        # Filtra vitórias
        victories = [game for game in all_history if game.is_victory()]
        
        # Se fornecido nome, filtra por jogador
        if player_name:
            victories = [
                game for game in victories
                if game.player_name.lower() == player_name.lower()
            ]
        
        return victories
    
    def get_defeats(self, player_name: str = None) -> List[GameHistory]:
        """
        Retorna todas as derrotas (opcionalmente de um jogador)
        
        Args:
            player_name: Nome do jogador (None = todos)
        
        Returns:
            Lista de derrotas
        """
        all_history = self.history_repository.get_all()
        
        # Filtra derrotas
        defeats = [game for game in all_history if game.is_defeat()]
        
        # Se fornecido nome, filtra por jogador
        if player_name:
            defeats = [
                game for game in defeats
                if game.player_name.lower() == player_name.lower()
            ]
        
        return defeats
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas gerais usando list comprehensions
        
        Returns:
            Dicionário com estatísticas:
            {
                'total_games': int,
                'total_wins': int,
                'total_losses': int,
                'win_rate': float,
                'average_attempts': float,
                'average_duration': float
            }
        """
        all_history = self.history_repository.get_all()
        
        if not all_history:
            return {
                'total_games': 0,
                'total_wins': 0,
                'total_losses': 0,
                'win_rate': 0.0,
                'average_attempts': 0.0,
                'average_duration': 0.0
            }
        
        total_games = len(all_history)
        
        # Calcula estatísticas
        total_wins = len([g for g in all_history if g.result == 'WIN'])
        total_losses = len([g for g in all_history if g.result == 'LOSS'])
        
        win_rate = (total_wins / total_games * 100) if total_games > 0 else 0.0
        
        # Calcula média de tentativas
        average_attempts = sum([g.attempts_used for g in all_history]) / total_games
        
        # Calcula média de duração
        average_duration = sum([g.duration_seconds for g in all_history]) / total_games
        
        return {
            'total_games': total_games,
            'total_wins': total_wins,
            'total_losses': total_losses,
            'win_rate': win_rate,
            'average_attempts': average_attempts,
            'average_duration': average_duration
        }
    
    def get_player_statistics(self, player_name: str) -> Dict[str, Any]:
        """
        Retorna estatísticas de um jogador específico
        
        Args:
            player_name: Nome do jogador
        
        Returns:
            Dicionário com estatísticas do jogador
        """
        player_games = self.get_player_history(player_name, limit=1000)
        
        if not player_games:
            return {
                'total_games': 0,
                'wins': 0,
                'losses': 0,
                'win_rate': 0.0,
                'average_attempts': 0.0,
                'best_performance': None
            }
        
        total = len(player_games)
        wins = len([g for g in player_games if g.is_victory()])
        losses = len([g for g in player_games if g.is_defeat()])
        
        win_rate = (wins / total * 100) if total > 0 else 0.0
        average_attempts = sum([g.attempts_used for g in player_games]) / total
        
        # Melhor performance (vitória com menos tentativas)
        victories = [g for g in player_games if g.is_victory()]
        best_performance = None
        
        if victories:
            best_performance = min(victories, key=lambda g: g.attempts_used)
        
        return {
            'total_games': total,
            'wins': wins,
            'losses': losses,
            'win_rate': win_rate,
            'average_attempts': average_attempts,
            'best_performance': best_performance
        }
    