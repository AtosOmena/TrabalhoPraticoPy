
import os
from typing import List
from domain.entities import GameHistory
from data.repositories import IHistoryRepository

class FileHistoryRepository(IHistoryRepository):
    """Repositório de histórico em arquivo texto"""
    
    def __init__(self, file_path: str = "assets/history.txt"):
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        #Cria o arquivo se não existir
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write("# Histórico - Formato: data|jogador|palavra|resultado|tentativas|duracao\n")
    
    def get_all(self) -> List[GameHistory]:
        #Lê todo o histórico
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            history = []
            for line in lines:
                if line.strip() and not line.startswith('#'):
                    try:
                        h = GameHistory.from_file_format(line)
                        history.append(h)
                    except Exception:
                        continue  # Ignora linhas inválidas
            
            return history
        
        except Exception as e:
            print(f"Erro ao ler histórico: {e}")
            return []
    
    def save(self, history: GameHistory) -> bool:
        #Adiciona registro ao histórico
        try:
            with open(self.file_path, 'a', encoding='utf-8') as f:
                f.write(history.to_file_format() + '\n')
            
            return True
        
        except Exception as e:
            print(f"Erro ao salvar histórico: {e}")
            return False
        