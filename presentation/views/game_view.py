
import tkinter as tk
from typing import Callable, Optional
from presentation.views import BaseView
from domain.entities import GameState

class GameView(BaseView):
    """Tela principal do jogo"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.on_guess: Optional[Callable] = None
        self.on_quit: Optional[Callable] = None
        
        self.word_label: Optional[tk.Label] = None
        self.attempts_label: Optional[tk.Label] = None
        self.guessed_label: Optional[tk.Label] = None
        self.letter_entry: Optional[tk.Entry] = None
        self.hangman_canvas: Optional[tk.Canvas] = None
    
    def _build_ui(self):
        """Constrói a interface"""
        # Header
        header = tk.Frame(self, bg='#34495E')
        header.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header,
            text="🎮 JOGO DA FORCA 🎮",
            font=("Arial", 20, "bold"),
            bg='#34495E',
            fg='#ECF0F1'
        ).pack(pady=10)
        
        # Container principal
        main_container = tk.Frame(self, bg='#2C3E50')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Canvas da forca (esquerda)
        canvas_frame = tk.Frame(main_container, bg='#2C3E50')
        canvas_frame.pack(side=tk.LEFT, padx=20)
        
        self.hangman_canvas = tk.Canvas(
            canvas_frame,
            width=300,
            height=350,
            bg='white',
            highlightthickness=2,
            highlightbackground='#3498DB'
        )
        self.hangman_canvas.pack()
        
        # Informações do jogo (direita)
        info_frame = tk.Frame(main_container, bg='#2C3E50')
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        
        # Palavra
        tk.Label(
            info_frame,
            text="Palavra:",
            font=("Arial", 14, "bold"),
            bg='#2C3E50',
            fg='#ECF0F1'
        ).pack(anchor='w', pady=(0, 5))
        
        self.word_label = tk.Label(
            info_frame,
            text="_ _ _ _ _",
            font=("Courier", 32, "bold"),
            bg='#34495E',
            fg='#ECF0F1',
            relief=tk.SUNKEN,
            bd=2
        )
        self.word_label.pack(fill=tk.X, pady=(0, 20))
        
        # Tentativas
        self.attempts_label = tk.Label(
            info_frame,
            text="❤️ Tentativas: 6/6",
            font=("Arial", 14, "bold"),
            bg='#2C3E50',
            fg='#27AE60'
        )
        self.attempts_label.pack(anchor='w', pady=5)
        
        # Letras já tentadas
        tk.Label(
            info_frame,
            text="Letras tentadas:",
            font=("Arial", 12),
            bg='#2C3E50',
            fg='#ECF0F1'
        ).pack(anchor='w', pady=(10, 5))
        
        self.guessed_label = tk.Label(
            info_frame,
            text="Nenhuma",
            font=("Arial", 12),
            bg='#34495E',
            fg='#95A5A6',
            relief=tk.SUNKEN,
            wraplength=300,
            justify=tk.LEFT
        )
        self.guessed_label.pack(fill=tk.X, pady=(0, 20))
        
        # Input de letra
        input_frame = tk.Frame(info_frame, bg='#2C3E50')
        input_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(
            input_frame,
            text="Digite uma letra:",
            font=("Arial", 12),
            bg='#2C3E50',
            fg='#ECF0F1'
        ).pack(anchor='w')
        
        entry_container = tk.Frame(input_frame, bg='#2C3E50')
        entry_container.pack(fill=tk.X, pady=5)
        
        self.letter_entry = tk.Entry(
            entry_container,
            font=("Arial", 18, "bold"),
            width=5,
            justify='center'
        )
        self.letter_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.letter_entry.bind('<Return>', lambda e: self._handle_guess())
        self.letter_entry.focus()
        
        tk.Button(
            entry_container,
            text="✓ Tentar",
            font=("Arial", 12, "bold"),
            bg='#3498DB',
            fg='white',
            width=10,
            command=self._handle_guess,
            cursor='hand2'
        ).pack(side=tk.LEFT)
        
        # Botão sair
        tk.Button(
            info_frame,
            text="◀ Sair do Jogo",
            font=("Arial", 12),
            bg='#E74C3C',
            fg='white',
            width=15,
            command=lambda: self.on_quit() if self.on_quit else None,
            cursor='hand2'
        ).pack(pady=20)
    
    def update_game_state(self, game_state: GameState):
        """Atualiza a view com o estado atual do jogo"""
        if not self.word_label:
            self._build_ui()
        
        # Atualiza palavra
        self.word_label.config(text=game_state.masked_word)
        
        # Atualiza tentativas
        remaining = game_state.remaining_attempts
        color = '#27AE60' if remaining > 3 else '#E67E22' if remaining > 1 else '#E74C3C'
        hearts = '❤️' * remaining + '🖤' * (6 - remaining)
        self.attempts_label.config(
            text=f"{hearts} Tentativas: {remaining}/6",
            fg=color
        )
        
        # Atualiza letras tentadas
        if game_state.guessed_letters:
            guessed_text = ', '.join(sorted(game_state.guessed_letters))
            self.guessed_label.config(text=guessed_text, fg='#ECF0F1')
        else:
            self.guessed_label.config(text="Nenhuma", fg='#95A5A6')
        
        # Desenha forca
        self._draw_hangman(game_state.wrong_attempts)
    
    def _draw_hangman(self, wrong_attempts: int):
        """Desenha o boneco da forca"""
        canvas = self.hangman_canvas
        canvas.delete("all")
        
        # Base
        canvas.create_line(50, 330, 250, 330, width=5, fill='#34495E')
        
        # Poste vertical
        canvas.create_line(100, 330, 100, 50, width=5, fill='#34495E')
        
        # Poste horizontal
        canvas.create_line(100, 50, 200, 50, width=5, fill='#34495E')
        
        # Corda
        canvas.create_line(200, 50, 200, 100, width=3, fill='#34495E')
        
        if wrong_attempts == 0:
            return
        
        # Cabeça
        if wrong_attempts >= 1:
            canvas.create_oval(175, 100, 225, 150, width=3, outline='#E74C3C')
        
        # Corpo
        if wrong_attempts >= 2:
            canvas.create_line(200, 150, 200, 220, width=3, fill='#E74C3C')
        
        # Braço esquerdo
        if wrong_attempts >= 3:
            canvas.create_line(200, 170, 170, 200, width=3, fill='#E74C3C')
        
        # Braço direito
        if wrong_attempts >= 4:
            canvas.create_line(200, 170, 230, 200, width=3, fill='#E74C3C')
        
        # Perna esquerda
        if wrong_attempts >= 5:
            canvas.create_line(200, 220, 170, 270, width=3, fill='#E74C3C')
        
        # Perna direita
        if wrong_attempts >= 6:
            canvas.create_line(200, 220, 230, 270, width=3, fill='#E74C3C')
            # X nos olhos
            canvas.create_line(185, 115, 195, 125, width=2, fill='black')
            canvas.create_line(195, 115, 185, 125, width=2, fill='black')
            canvas.create_line(205, 115, 215, 125, width=2, fill='black')
            canvas.create_line(215, 115, 205, 125, width=2, fill='black')
    
    def _handle_guess(self):
        """Processa tentativa de letra"""
        letter = self.letter_entry.get().strip()
        self.letter_entry.delete(0, tk.END)
        
        if self.on_guess:
            self.on_guess(letter)
    
    def show_message(self, message: str, is_error: bool = False):
        """Exibe mensagem temporária"""
        color = '#E74C3C' if is_error else '#27AE60'
        # Poderia adicionar um label temporário aqui
