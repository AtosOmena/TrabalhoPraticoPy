"""
Camada de Apresentação - Controllers
Faz a ponte entre Views (UI) e Use Cases (Lógica)
"""

import threading
from tkinter import messagebox
from domain.use_cases import HangmanGameUseCase, ScoreboardUseCase, HistoryUseCase
from presentation.views import (
    MainMenuView, PlayerSetupView, GameView, 
    GameOverView, ScoreboardView, HistoryView
)

class GameController:
    """
    Controlador principal da aplicação
    Gerencia navegação entre telas e coordena use cases
    """
    
    def __init__(self, root, game_use_case: HangmanGameUseCase, 
                 scoreboard_use_case: ScoreboardUseCase,
                 history_use_case: HistoryUseCase):
        self.root = root
        self.game_use_case = game_use_case
        self.scoreboard_use_case = scoreboard_use_case
        self.history_use_case = history_use_case
        
        # Views
        self.main_menu = MainMenuView(root)
        self.player_setup = PlayerSetupView(root)
        self.game_view = GameView(root)
        self.game_over = GameOverView(root)
        self.scoreboard = ScoreboardView(root)
        self.history = HistoryView(root)
        
        self.current_view = None
        
        # Configura callbacks das views
        self._setup_view_callbacks()
        
        # Mostra menu principal
        self.show_main_menu()
    
    def _setup_view_callbacks(self):
        """Configura os callbacks de todas as views"""
        # Main Menu
        self.main_menu.on_single_player = self._start_single_player_setup
        self.main_menu.on_multiplayer = self._start_multiplayer_setup
        self.main_menu.on_scoreboard = self.show_scoreboard
        self.main_menu.on_history = self.show_history
        
        # Player Setup
        self.player_setup.on_start = self._handle_game_start
        self.player_setup.on_back = self.show_main_menu
        
        # Game View
        self.game_view.on_guess = self._handle_guess
        self.game_view.on_quit = self._quit_game
        
        # Game Over
        self.game_over.on_play_again = self._play_again
        self.game_over.on_menu = self.show_main_menu
        
        # Scoreboard
        self.scoreboard.on_back = self.show_main_menu
        
        # History
        self.history.on_back = self.show_main_menu
    
    def _switch_view(self, new_view):
        """Troca a view atual"""
        if self.current_view:
            self.current_view.hide()
        
        new_view.show()
        self.current_view = new_view
        
        self.root.update_idletasks()
    
    # ==================== Navegação ====================
    
    def show_main_menu(self):
        """Exibe menu principal"""
        self.game_use_case.reset_game()
        self._switch_view(self.main_menu)
    
    def _start_single_player_setup(self):
        """Inicia configuração single player"""
        self.player_setup.setup_for_mode(multiplayer=False)
        self._switch_view(self.player_setup)
    
    def _start_multiplayer_setup(self):
        """Inicia configuração multiplayer"""
        self.player_setup.setup_for_mode(multiplayer=True)
        self._switch_view(self.player_setup)
    
    def show_scoreboard(self):
        """Exibe placar"""
        def load_ranking():
            ranking = self.scoreboard_use_case.get_ranking(limit=20)
            self.root.after(0, lambda: self._display_scoreboard(ranking))
        
        threading.Thread(target=load_ranking, daemon=True).start()
    
    def _display_scoreboard(self, ranking):
        """Exibe o placar após carregamento"""
        self.scoreboard.show_ranking(ranking)
        self._switch_view(self.scoreboard)
    
    def show_history(self):
        """Exibe histórico"""
        def load_history():
            recent_games = self.history_use_case.get_recent_games(limit=30)
            stats = self.history_use_case.get_statistics()
            self.root.after(0, lambda: self._display_history(recent_games, stats))
        
        threading.Thread(target=load_history, daemon=True).start()
    
    def _display_history(self, recent_games, stats):
        """Exibe o histórico após carregamento"""
        self.history.show_history(recent_games, stats)
        self._switch_view(self.history)
    
    # ==================== Lógica do Jogo ====================
    
    def _handle_game_start(self, *args):
        """Inicia o jogo com base nos parâmetros"""
        try:
            if len(args) == 1:
                # Single player
                player_name = args[0]
                game_state = self.game_use_case.start_single_player_game(player_name)
            else:
                # Multiplayer
                player1, player2, word = args
                game_state = self.game_use_case.start_multiplayer_game(
                    player1, player2, word
                )
            
            self.game_view.update_game_state(game_state)
            self._switch_view(self.game_view)
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar jogo: {str(e)}")
    
    def _handle_guess(self, letter: str):
        """Processa tentativa de letra"""
        try:
            result = self.game_use_case.make_guess(letter)
            
            if not result['valid']:
                messagebox.showwarning("Aviso", result['message'])
                return
            
            # Atualiza view
            game_state = result['game_state']
            self.game_view.update_game_state(game_state)
            
            # Verifica fim do jogo
            if result['game_over']:
                self.root.after(1000, lambda: self._show_game_over(game_state))
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar tentativa: {str(e)}")
    
    def _show_game_over(self, game_state):
        """Exibe tela de game over"""
        def save_and_show():
            # Apenas exibe a tela
            self.root.after(0, lambda: self._display_game_over(game_state))
        
        threading.Thread(target=save_and_show, daemon=True).start()
    
    def _display_game_over(self, game_state):
        """Exibe a tela de game over após processamento"""
        self.game_over.show_result(game_state)
        self._switch_view(self.game_over)
    
    def _quit_game(self):
        """Sai do jogo atual"""
        if messagebox.askyesno("Confirmar", "Deseja realmente sair do jogo?"):
            self.show_main_menu()
    
    def _play_again(self):
        """Joga novamente"""
        self.show_main_menu()