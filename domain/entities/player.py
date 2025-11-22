
class Player:
    """Representa um jogador com score e estatísticas"""
    
    def __init__(self, name: str, wins: int = 0, losses: int = 0):
        self.name = name
        self.wins = wins
        self.losses = losses
    
    @property
    def total_games(self) -> int:
        return self.wins + self.losses
    
    @property
    def win_rate(self) -> float:
        if self.total_games == 0:
            return 0.0
        return (self.wins / self.total_games) * 100
    
    # Métodos Mágicos
    def __str__(self) -> str:
        """Representação textual do jogador"""
        return f"{self.name}: {self.wins}V/{self.losses}D (WR: {self.win_rate:.1f}%)"
    
    def __repr__(self) -> str:
        return f"Player(name='{self.name}', wins={self.wins}, losses={self.losses})"
    
    def __gt__(self, other: 'Player') -> bool:
        """Comparação para ordenar por vitórias (decrescente)"""
        if self.wins != other.wins:
            return self.wins > other.wins
        return self.win_rate > other.win_rate
    
    def __lt__(self, other: 'Player') -> bool:
        """Comparação menor que"""
        return not self.__gt__(other) and self != other
    
    def __eq__(self, other: object) -> bool:
        """Igualdade baseada no nome"""
        if not isinstance(other, Player):
            return False
        return self.name.lower() == other.name.lower()
    
    def __hash__(self) -> int:
        """Hash para uso em dicionários"""
        return hash(self.name.lower())
    
    def __add__(self, other: 'Player') -> 'Player':
        """Combina estatísticas de dois jogadores (mesmo nome)"""
        if self.name.lower() != other.name.lower():
            raise ValueError("Não é possível somar jogadores diferentes")
        return Player(
            name=self.name,
            wins=self.wins + other.wins,
            losses=self.losses + other.losses
        )
