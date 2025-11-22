"""
Use Case: HangmanGameUseCase
Single Responsibility: Orquestrar o fluxo principal do jogo
"""

import random
import threading
from typing import Optional, Dict, Any

from domain.entities.game_state import GameState
from domain.entities.player import Player
from domain.entities.game_history import GameHistory


class HangmanGameUseCase:
    """
    Caso de uso principal: gerencia o fluxo do jogo
    """
    
    def __init__(self, word_repository, player_repository, history_repository):
        """
        Args:
            word_repository: Implementação de IWordRepository
            player_repository: Implementação de IPlayerRepository
            history_repository: Implementação de IHistoryRepository
        """
        self.word_repository = word_repository
        self.player_repository = player_repository
        self.history_repository = history_repository
        self.current_game: Optional[GameState] = None
    
    
    
    def start_single_player_game(self, player_name: str) -> GameState:
        """
        Inicia um jogo single player com palavra aleatória
        
        Args:
            player_name: Nome do jogador
        
        Returns:
            Estado inicial do jogo
        
        Raises:
            ValueError: Se nome do jogador for inválido
        """
        if not player_name or not player_name.strip():
            raise ValueError("Nome do jogador não pode ser vazio")
        
        word = self._get_random_word()
        self.current_game = GameState(word=word, player_name=player_name.strip())
        
        return self.current_game
    
    def start_multiplayer_game(
        self, 
        player1_name: str, 
        player2_name: str, 
        word: str
    ) -> GameState:
        """
        Inicia um jogo multiplayer onde player1 escolhe a palavra
        e player2 adivinha
        
        Args:
            player1_name: Nome do jogador que escolhe a palavra
            player2_name: Nome do jogador que adivinha
            word: Palavra escolhida por player1
        
        Returns:
            Estado inicial do jogo
        
        Raises:
            ValueError: Se parâmetros forem inválidos
        """

        # Validações
        if not player1_name or not player1_name.strip():
            raise ValueError("Nome do Jogador 1 não pode ser vazio")
        
        if not player2_name or not player2_name.strip():
            raise ValueError("Nome do Jogador 2 não pode ser vazio")
        
        if not word or len(word.strip()) < 3:
            raise ValueError("A palavra deve ter pelo menos 3 caracteres")
        
        if not word.strip().isalpha():
            raise ValueError("A palavra deve conter apenas letras")
        
        # Player2 é quem adivinha
        self.current_game = GameState(
            word=word.strip(), 
            player_name=player2_name.strip()
        )
        
        return self.current_game
    
    
    
    def make_guess(self, letter: str) -> Dict[str, Any]:
        """
        Processa um palpite de letra
        
        Args:
            letter: Letra a ser tentada
        
        Returns:
            Dicionário com resultado e estado atual:
            {
                'valid': bool,          # Se a tentativa é válida
                'correct': bool,        # Se a letra está na palavra
                'message': str,         # Mensagem de feedback
                'game_state': GameState,# Estado atual do jogo
                'game_over': bool,      # Se o jogo terminou
                'won': bool             # Se o jogador venceu
            }
        
        Raises:
            RuntimeError: Se não há jogo em andamento
        """
        if not self.current_game:
            raise RuntimeError("Nenhum jogo em andamento")
        
        if self.current_game.is_game_over:
            raise RuntimeError("O jogo já terminou")
        
        # Validação da letra
        if not letter or len(letter) != 1 or not letter.isalpha():
            return {
                'valid': False,
                'correct': False,
                'message': 'Digite apenas uma letra válida',
                'game_state': self.current_game,
                'game_over': False,
                'won': False
            }
        
        letter = letter.upper()
        
        # Verifica se já foi tentada
        if letter in self.current_game:
            return {
                'valid': False,
                'correct': False,
                'message': f'A letra {letter} já foi tentada',
                'game_state': self.current_game,
                'game_over': False,
                'won': False
            }
        
        # Processa tentativa
        is_correct = self.current_game.guess_letter(letter)
        
        # Verifica se o jogo terminou
        game_over = self.current_game.is_game_over
        
        if game_over:
            self._finish_game()
        
        return {
            'valid': True,
            'correct': is_correct,
            'message': f'Letra {letter} {"correta!" if is_correct else "incorreta!"}',
            'game_state': self.current_game,
            'game_over': game_over,
            'won': self.current_game.is_won
        }
    
    
    
    def _finish_game(self) -> None:
        """
        Finaliza o jogo atual e persiste dados
        - Salva histórico da partida
        - Atualiza estatísticas do jogador
        """
        if not self.current_game:
            return
        
        self.current_game.finish_game()
        
        # Captura dados antes da thread
        history = GameHistory.from_game_state(self.current_game)
        player_name = self.current_game.player_name
        won = self.current_game.is_won
        
        # FIX: Executa I/O em background
        def save_data():
            self.history_repository.save(history)
            self.player_repository.save_game_result(player_name, won)
        
        threading.Thread(target=save_data, daemon=True).start()
    
    def _get_random_word(self) -> str:
        """
        Obtém palavra aleatória do repositório
        
        Returns:
            Palavra aleatória em maiúsculas
        """
        words = self.word_repository.get_all()
        
        if not words:
            # Fallback: lista básica caso o arquivo não exista
            words = [
                'PYTHON', 'PROGRAMACAO', 'COMPUTADOR', 'DESENVOLVEDOR', 
                'ALGORITMO', 'ARQUITETURA', 'ENGENHARIA', 'SOFTWARE'
            ]
        
        return random.choice(words)
    
    
    
    def get_current_game(self) -> Optional[GameState]:
        """Retorna o jogo atual (ou None se não houver)"""
        return self.current_game
    
    def reset_game(self) -> None:
        """Reseta o jogo atual"""
        self.current_game = None
