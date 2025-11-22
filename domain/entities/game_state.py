
from datetime import datetime
from typing import List, Optional

class GameState:
    """Representa o estado atual do jogo da forca"""
    
    MAX_ATTEMPTS = 6  # Número máximo de erros permitidos
    
    def __init__(self, word: str, player_name: str):
        self.word = word.upper()
        self.player_name = player_name
        self.guessed_letters: set = set()
        self.wrong_attempts = 0
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None
    
    @property
    def remaining_attempts(self) -> int:
        """Tentativas restantes"""
        return self.MAX_ATTEMPTS - self.wrong_attempts
    
    @property
    def is_game_over(self) -> bool:
        """Verifica se o jogo terminou"""
        return self.is_won or self.is_lost
    
    @property
    def is_won(self) -> bool:
        """Verifica se o jogador venceu"""
        return all(letter in self.guessed_letters for letter in self.word)
    
    @property
    def is_lost(self) -> bool:
        """Verifica se o jogador perdeu"""
        return self.wrong_attempts >= self.MAX_ATTEMPTS
    
    @property
    def masked_word(self) -> str:
        """Retorna a palavra com letras não descobertas mascaradas"""
        return ' '.join([
            letter if letter in self.guessed_letters else '_'
            for letter in self.word
        ])
    
    @property
    def all_letters_guessed(self) -> List[str]:
        """Lista ordenada de todas as letras tentadas"""
        return sorted(list(self.guessed_letters))
    
    @property
    def wrong_letters(self) -> List[str]:
        """Lista de letras erradas"""
        return sorted([
            letter for letter in self.guessed_letters 
            if letter not in self.word
        ])
    
    def guess_letter(self, letter: str) -> bool:
        """
        Processa um palpite de letra
        Retorna True se a letra estava na palavra, False caso contrário
        """
        letter = letter.upper()
        
        if letter in self.guessed_letters:
            return False  # Letra já foi tentada
        
        self.guessed_letters.add(letter)
        
        if letter not in self.word:
            self.wrong_attempts += 1
            return False
        
        return True
    
    def finish_game(self):
        """Marca o fim do jogo"""
        self.end_time = datetime.now()
    
    @property
    def duration_seconds(self) -> int:
        """Duração da partida em segundos"""
        end = self.end_time or datetime.now()
        return int((end - self.start_time).total_seconds())
    
    # Métodos Mágicos
    def __str__(self) -> str:
        """Representação textual do estado do jogo"""
        status = "Vitória" if self.is_won else "Derrota" if self.is_lost else "Em andamento"
        return (f"Jogador: {self.player_name} | Palavra: {self.masked_word} | "
                f"Tentativas: {self.wrong_attempts}/{self.MAX_ATTEMPTS} | Status: {status}")
    
    def __len__(self) -> int:
        """Retorna o tamanho da palavra"""
        return len(self.word)
    
    def __repr__(self) -> str:
        return f"GameState(word='{self.word}', player='{self.player_name}', attempts={self.wrong_attempts})"
    
    def __contains__(self, letter: str) -> bool:
        """Verifica se uma letra foi tentada"""
        return letter.upper() in self.guessed_letters
