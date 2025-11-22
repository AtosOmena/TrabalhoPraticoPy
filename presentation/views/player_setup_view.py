
import tkinter as tk
from typing import Callable, Optional
from presentation.views import BaseView
from tkinter import messagebox

class PlayerSetupView(BaseView):
    """Tela de configuração de jogadores"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.on_start: Optional[Callable] = None
        self.on_back: Optional[Callable] = None
        self.multiplayer_mode = False
        
        self.player1_entry: Optional[tk.Entry] = None
        self.player2_entry: Optional[tk.Entry] = None
        self.word_entry: Optional[tk.Entry] = None
    
    def setup_for_mode(self, multiplayer: bool):
        """Configura a view para o modo escolhido"""
        self.multiplayer_mode = multiplayer
        self.clear()
        self._build_ui()
    
    def _build_ui(self):
        """Constrói a interface"""
        # Título
        title = "Configuração Multiplayer" if self.multiplayer_mode else "Configuração Single Player"
        tk.Label(
            self,
            text=title,
            font=("Arial", 24, "bold"),
            bg='#2C3E50',
            fg='#ECF0F1'
        ).pack(pady=30)
        
        # Formulário
        form_frame = tk.Frame(self, bg='#2C3E50')
        form_frame.pack(pady=20)
        
        # Player 1 / Único jogador
        player_label = "Jogador 1 (escolhe palavra):" if self.multiplayer_mode else "Nome do Jogador:"
        tk.Label(
            form_frame,
            text=player_label,
            font=("Arial", 14),
            bg='#2C3E50',
            fg='#ECF0F1'
        ).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        
        self.player1_entry = tk.Entry(form_frame, font=("Arial", 14), width=25)
        self.player1_entry.grid(row=0, column=1, padx=10, pady=10)
        self.player1_entry.focus()
        
        # Player 2 e Palavra (apenas multiplayer)
        if self.multiplayer_mode:
            tk.Label(
                form_frame,
                text="Jogador 2 (adivinha):",
                font=("Arial", 14),
                bg='#2C3E50',
                fg='#ECF0F1'
            ).grid(row=1, column=0, padx=10, pady=10, sticky='e')
            
            self.player2_entry = tk.Entry(form_frame, font=("Arial", 14), width=25)
            self.player2_entry.grid(row=1, column=1, padx=10, pady=10)
            
            tk.Label(
                form_frame,
                text="Palavra secreta:",
                font=("Arial", 14),
                bg='#2C3E50',
                fg='#ECF0F1'
            ).grid(row=2, column=0, padx=10, pady=10, sticky='e')
            
            self.word_entry = tk.Entry(form_frame, font=("Arial", 14), width=25, show='*')
            self.word_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Botões
        button_frame = tk.Frame(self, bg='#2C3E50')
        button_frame.pack(pady=30)
        
        tk.Button(
            button_frame,
            text="▶ Iniciar Jogo",
            font=("Arial", 14, "bold"),
            bg='#27AE60',
            fg='white',
            width=15,
            height=2,
            command=self._handle_start,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            button_frame,
            text="◀ Voltar",
            font=("Arial", 14),
            bg='#E74C3C',
            fg='white',
            width=15,
            height=2,
            command=lambda: self.on_back() if self.on_back else None,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=10)
    
    def _handle_start(self):
        """Processa o início do jogo"""
        player1_name = self.player1_entry.get().strip()
        
        if not player1_name:
            messagebox.showwarning("Aviso", "Digite o nome do jogador!")
            return
        
        if self.multiplayer_mode:
            player2_name = self.player2_entry.get().strip()
            word = self.word_entry.get().strip()
            
            if not player2_name:
                messagebox.showwarning("Aviso", "Digite o nome do Jogador 2!")
                return
            
            if not word or len(word) < 3:
                messagebox.showwarning("Aviso", "A palavra deve ter pelo menos 3 letras!")
                return
            
            if self.on_start:
                self.on_start(player1_name, player2_name, word)
        else:
            if self.on_start:
                self.on_start(player1_name)
