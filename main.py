"""
Ponto de Entrada da Aplicação
Responsável por:
1. Configurar as dependências (Dependency Injection)
2. Instanciar repositórios, use cases e controllers
3. Inicializar a aplicação Tkinter
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Adiciona o diretório raiz ao path para imports absolutos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importações das camadas
from data.storage import FileWordRepository, FilePlayerRepository, FileHistoryRepository
from domain.use_cases import HangmanGameUseCase, ScoreboardUseCase, HistoryUseCase
from presentation.controllers.game_controller import GameController


class HangmanApplication:
    """
    Classe principal da aplicação
    Aplica Injeção de Dependências e Clean Architecture
    """
    
    def __init__(self):
        # Configuração da janela principal
        self.root = tk.Tk()
        self.root.title("Jogo da Forca")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Centraliza janela na tela
        self._center_window()
        
        # Configuração de estilo
        self._setup_styles()
        
        # Dependency Injection - Camada de Dados (Repositórios)
        self.word_repository = FileWordRepository("assets/words.txt")
        self.player_repository = FilePlayerRepository("assets/scoreboard.txt")
        self.history_repository = FileHistoryRepository("assets/history.txt")
        
        # Dependency Injection - Camada de Domínio (Use Cases)
        self.game_use_case = HangmanGameUseCase(
            word_repository=self.word_repository,
            player_repository=self.player_repository,
            history_repository=self.history_repository
        )
        
        self.scoreboard_use_case = ScoreboardUseCase(
            player_repository=self.player_repository
        )
        
        self.history_use_case = HistoryUseCase(
            history_repository=self.history_repository
        )
        
        # Dependency Injection - Camada de Apresentação (Controller)
        self.controller = GameController(
            root=self.root,
            game_use_case=self.game_use_case,
            scoreboard_use_case=self.scoreboard_use_case,
            history_use_case=self.history_use_case
        )
    
    def _center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _setup_styles(self):
        """Configura estilos globais"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurações de cores
        self.root.configure(bg='#2C3E50')

        if sys.platform == 'darwin':
            self.root.update_idletasks()
    
    def run(self):
        """Inicia o loop principal da aplicação"""
        
        # Inicia loop do Tkinter
        self.root.mainloop()


def main():
    """Função principal"""
    try:
        app = HangmanApplication()
        app.run()
    except Exception as e:
        print(f"\n Erro ao iniciar aplicação: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()