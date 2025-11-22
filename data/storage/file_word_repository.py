
import os
from typing import List
from data.repositories import IWordRepository

class FileWordRepository(IWordRepository):
    """Repositório de palavras em arquivo texto"""
    
    def __init__(self, file_path: str = "assets/words.txt"):
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        #Cria o arquivo com palavras padrão se não existir
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        if not os.path.exists(self.file_path):
            default_words = [
                'PYTHON', 'JAVASCRIPT', 'PROGRAMACAO', 'COMPUTADOR',
                'DESENVOLVEDOR', 'ALGORITMO', 'ARQUITETURA', 'ENGENHARIA',
                'SOFTWARE', 'HARDWARE', 'INTERNET', 'TECNOLOGIA',
                'INTELIGENCIA', 'ARTIFICIAL', 'MACHINE', 'LEARNING',
                'DATABASE', 'FRAMEWORK', 'BIBLIOTECA', 'INTERFACE',
                'BACKEND', 'FRONTEND', 'FULLSTACK', 'DEVOPS',
                'SERVIDOR', 'CLIENTE', 'PROTOCOLO', 'SEGURANCA',
                'CRIPTOGRAFIA', 'COMPILADOR', 'INTERPRETADOR', 'DEBUGGER'
            ]
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(default_words))
    
    def get_all(self) -> List[str]:
        #Lê todas as palavras do arquivo
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:

                words = [
                    line.strip().upper() 
                    for line in f.readlines() 
                    if line.strip() and line.strip().isalpha()
                ]
                return words
        except Exception as e:
            print(f"Erro ao ler palavras: {e}")
            return []
    
    def add_word(self, word: str) -> bool:
        #Adiciona nova palavra ao arquivo
        try:
            word = word.strip().upper()
            if not word or not word.isalpha():
                return False
            
            # Verifica se já existe
            existing = self.get_all()
            if word in existing:
                return False
            
            with open(self.file_path, 'a', encoding='utf-8') as f:
                f.write(f'\n{word}')
            
            return True
        except Exception as e:
            print(f"Erro ao adicionar palavra: {e}")
            return False
