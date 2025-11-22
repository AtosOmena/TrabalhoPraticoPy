
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, List
from presentation.views import BaseView
from domain.entities import Player

class ScoreboardView(BaseView):
    """Tela de placar"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.on_back: Optional[Callable] = None
    
    def show_ranking(self, players: List[Player]):
        """Exibe ranking de jogadores"""
        self.clear()
        
        # Título
        tk.Label(
            self,
            text="🏆 PLACAR 🏆",
            font=("Arial", 28, "bold"),
            bg='#2C3E50',
            fg='#F39C12'
        ).pack(pady=20)
        
        # Tabela
        table_frame = tk.Frame(self, bg='#2C3E50')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
        
        # Cabeçalho
        header = tk.Frame(table_frame, bg='#34495E', relief=tk.RAISED, bd=2)
        header.pack(fill=tk.X, pady=(0, 10))
        
        headers = ["#", "Jogador", "Vitórias", "Derrotas", "WR%"]
        widths = [5, 25, 12, 12, 10]
        
        for i, (text, width) in enumerate(zip(headers, widths)):
            tk.Label(
                header,
                text=text,
                font=("Arial", 12, "bold"),
                bg='#34495E',
                fg='#ECF0F1',
                width=width
            ).grid(row=0, column=i, padx=5, pady=10)
        
        # Container com scroll
        canvas_container = tk.Frame(table_frame)
        canvas_container.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(canvas_container, bg='#2C3E50', highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2C3E50')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Linhas de jogadores
        medals = ['🥇', '🥈', '🥉']
        
        for idx, player in enumerate(players, 1):
            row_bg = '#34495E' if idx % 2 == 0 else '#2C3E50'
            row = tk.Frame(scrollable_frame, bg=row_bg, relief=tk.FLAT)
            row.pack(fill=tk.X, pady=2)
            
            medal = medals[idx-1] if idx <= 3 else str(idx)
            
            values = [
                medal,
                player.name,
                str(player.wins),
                str(player.losses),
                f"{player.win_rate:.1f}%"
            ]
            
            for i, (value, width) in enumerate(zip(values, widths)):
                tk.Label(
                    row,
                    text=value,
                    font=("Arial", 11),
                    bg=row_bg,
                    fg='#ECF0F1',
                    width=width
                ).grid(row=0, column=i, padx=5, pady=8)
        
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

