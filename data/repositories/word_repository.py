"""
Interface: IWordRepository
Definir contrato para repositório de palavras
"""

from abc import ABC, abstractmethod
from typing import List


class IWordRepository(ABC):
    """
    Interface para repositório de palavras
    Define operações abstratas para gerenciar o dicionário de palavras
    """
    
    @abstractmethod
    def get_all(self) -> List[str]:
        """
        Retorna todas as palavras disponíveis
        
        Returns:
            Lista de palavras em maiúsculas
        """
        pass
    
    @abstractmethod
    def add_word(self, word: str) -> bool:
        """
        Adiciona uma nova palavra ao repositório
        
        Args:
            word: Palavra a ser adicionada
        
        Returns:
            True se adicionada com sucesso, False se já existe ou erro
        """
        pass
    