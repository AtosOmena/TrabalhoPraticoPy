
import tkinter as tk
from typing import Callable, Optional
from presentation.views import BaseView

class MainMenuView(BaseView):
    """Tela de menu principal"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.on_single_player: Optional[Callable] = None
        self.on_multiplayer: Optional[Callable] = None
        self.on_scoreboard: Optional[Callable] = None
        self.on_history: Optional[Callable] = None
        self._build_ui()
    
    def _build_ui(self):
        """Constrói a interface"""
        # Título
        title_frame = tk.Frame(self, bg='#2C3E50')
        title_frame.pack(pady=50)
        
        tk.Label(
            title_frame,
            text="🎮 JOGO DA FORCA 🎮",
            font=("Arial", 36, "bold"),
            bg='#2C3E50',
            fg='#ECF0F1'
        ).pack()
        
        tk.Label(
            title_frame,
            text="by Atos",
            font=("Arial", 14, "italic"),
            bg='#2C3E50',
            fg='#95A5A6'
        ).pack()
        
        # Botões
        button_frame = tk.Frame(self, bg='#2C3E50')
        button_frame.pack(pady=30)
        
        button_style = {
            'font': ("Arial", 16, "bold"),
            'width': 20,
            'height': 2,
            'bg': '#3498DB',
            'fg': 'white',
            'activebackground': '#2980B9',
            'cursor': 'hand2',
            'relief': tk.RAISED,
            'bd': 3
        }
        
        tk.Button(
            button_frame,
            text="🎯 Single Player",
            command=lambda: self.on_single_player() if self.on_single_player else None,
            **button_style
        ).pack(pady=10)
        
        tk.Button(
            button_frame,
            text="👥 Multiplayer (1v1)",
            command=lambda: self.on_multiplayer() if self.on_multiplayer else None,
            **button_style
        ).pack(pady=10)
        
        tk.Button(
            button_frame,
            text="🏆 Placar",
            command=lambda: self.on_scoreboard() if self.on_scoreboard else None,
            bg='#E67E22',
            activebackground='#D35400',
            **{k: v for k, v in button_style.items() if k not in ['bg', 'activebackground']}
        ).pack(pady=10)
        
        tk.Button(
            button_frame,
            text="📜 Histórico",
            command=lambda: self.on_history() if self.on_history else None,
            bg='#9B59B6',
            activebackground='#8E44AD',
            **{k: v for k, v in button_style.items() if k not in ['bg', 'activebackground']}
        ).pack(pady=10)
