
import tkinter as tk
from typing import Callable, Optional
from domain.entities import GameState
from presentation.views import BaseView

class GameOverView(BaseView):
    """Tela de fim de jogo"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.on_play_again: Optional[Callable] = None
        self.on_menu: Optional[Callable] = None
    
    def show_result(self, game_state: GameState):
        """Exibe resultado do jogo"""
        self.clear()
        
        won = game_state.is_won
        
        # Título
        title_text = "🎉 VITÓRIA! 🎉" if won else "😢 GAME OVER 😢"
        title_color = '#27AE60' if won else '#E74C3C'
        
        tk.Label(
            self,
            text=title_text,
            font=("Arial", 36, "bold"),
            bg='#2C3E50',
            fg=title_color
        ).pack(pady=30)
        
        # Informações
        info_frame = tk.Frame(self, bg='#34495E', relief=tk.RAISED, bd=3)
        info_frame.pack(pady=20, padx=50, fill=tk.X)
        
        info_data = [
            ("Jogador:", game_state.player_name),
            ("Palavra:", game_state.word),
            ("Tentativas usadas:", f"{game_state.wrong_attempts}/6"),
            ("Duração:", f"{game_state.duration_seconds} segundos")
        ]
        
        for label, value in info_data:
            row = tk.Frame(info_frame, bg='#34495E')
            row.pack(fill=tk.X, padx=20, pady=5)
            
            tk.Label(
                row,
                text=label,
                font=("Arial", 14, "bold"),
                bg='#34495E',
                fg='#ECF0F1'
            ).pack(side=tk.LEFT)
            
            tk.Label(
                row,
                text=value,
                font=("Arial", 14),
                bg='#34495E',
                fg='#3498DB'
            ).pack(side=tk.RIGHT)
        
        # Botões
        button_frame = tk.Frame(self, bg='#2C3E50')
        button_frame.pack(pady=40)
        
        tk.Button(
            button_frame,
            text="🔄 Jogar Novamente",
            font=("Arial", 14, "bold"),
            bg='#3498DB',
            fg='white',
            width=20,
            height=2,
            command=lambda: self.on_play_again() if self.on_play_again else None,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            button_frame,
            text="🏠 Menu Principal",
            font=("Arial", 14, "bold"),
            bg='#95A5A6',
            fg='white',
            width=20,
            height=2,
            command=lambda: self.on_menu() if self.on_menu else None,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=10)
