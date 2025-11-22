
import tkinter as tk
from tkinter import scrolledtext
from typing import Callable, Optional, List
from presentation.views import BaseView
from domain.entities import GameHistory

class HistoryView(BaseView):
    """Tela de histórico"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.on_back: Optional[Callable] = None
    
    def show_history(self, history: List[GameHistory], stats: dict):
        """Exibe histórico de partidas"""
        self.clear()
        
        # Título
        tk.Label(
            self,
            text="📜 HISTÓRICO 📜",
            font=("Arial", 28, "bold"),
            bg='#2C3E50',
            fg='#9B59B6'
        ).pack(pady=20)
        
        # Estatísticas gerais
        stats_frame = tk.Frame(self, bg='#34495E', relief=tk.RAISED, bd=2)
        stats_frame.pack(fill=tk.X, padx=50, pady=(0, 20))
        
        stats_data = [
            ("Total de Jogos:", stats['total_games']),
            ("Vitórias:", f"{stats['total_wins']} ({stats['win_rate']:.1f}%)"),
            ("Derrotas:", stats['total_losses']),
            ("Média de Tentativas:", f"{stats['average_attempts']:.1f}")
        ]
        
        for label, value in stats_data:
            row = tk.Frame(stats_frame, bg='#34495E')
            row.pack(fill=tk.X, padx=20, pady=5)
            
            tk.Label(
                row,
                text=label,
                font=("Arial", 12, "bold"),
                bg='#34495E',
                fg='#ECF0F1'
            ).pack(side=tk.LEFT)
            
            tk.Label(
                row,
                text=str(value),
                font=("Arial", 12),
                bg='#34495E',
                fg='#3498DB'
            ).pack(side=tk.RIGHT)
        
        # Lista de histórico com scroll
        list_frame = tk.Frame(self, bg='#2C3E50')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=50)
        
        scrolled_text = scrolledtext.ScrolledText(
            list_frame,
            font=("Courier", 10),
            bg='#34495E',
            fg='#ECF0F1',
            wrap=tk.WORD,
            height=15
        )
        scrolled_text.pack(fill=tk.BOTH, expand=True)
        
        for game in history:
            scrolled_text.insert(tk.END, str(game) + "\n")
        
        scrolled_text.config(state=tk.DISABLED)
        
        # Botão voltar
        tk.Button(
            self,
            text="◀ Voltar",
            font=("Arial", 14, "bold"),
            bg='#3498DB',
            fg='white',
            width=15,
            height=2,
            command=lambda: self.on_back() if self.on_back else None,
            cursor='hand2'
        ).pack(pady=20)