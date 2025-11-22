
import os
from typing import List, Optional
from domain.entities import Player
from data.repositories import IPlayerRepository

class FilePlayerRepository(IPlayerRepository):
    """Repositório de jogadores em arquivo texto"""
    
    def __init__(self, file_path: str = "assets/scoreboard.txt"):
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        #Cria o arquivo se não existir
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write("# Placar - Formato: nome|vitorias|derrotas\n")
    
    def get_all(self) -> List[Player]:
        #Lê todos os jogadores do arquivo
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            players = [
                self._parse_player_line(line)
                for line in lines
                if line.strip() and not line.startswith('#')
            ]
            
            # Filtra None
            return [p for p in players if p is not None]
        
        except Exception as e:
            print(f"Erro ao ler jogadores: {e}")
            return []
    
    def get_by_name(self, name: str) -> Optional[Player]:
        #Busca jogador por nome
        all_players = self.get_all()
        
        # List comprehension com filtro
        matches = [p for p in all_players if p.name.lower() == name.lower()]
        
        return matches[0] if matches else None
    
    def save(self, player: Player) -> bool:
        #Salva ou atualiza jogador
        try:
            all_players = self.get_all()
            
            # Atualiza se existe, adiciona se não
            player_exists = False
            for i, p in enumerate(all_players):
                if p.name.lower() == player.name.lower():
                    all_players[i] = player
                    player_exists = True
                    break
            
            if not player_exists:
                all_players.append(player)
            
            # Reescreve arquivo
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write("# Placar - Formato: nome|vitorias|derrotas\n")
                for p in all_players:
                    f.write(f"{p.name}|{p.wins}|{p.losses}\n")
            
            return True
        
        except Exception as e:
            print(f"Erro ao salvar jogador: {e}")
            return False
    
    def save_game_result(self, player_name: str, won: bool) -> bool:
        #Salva resultado de uma partida
        player = self.get_by_name(player_name)
        
        if player is None:
            player = Player(name=player_name)
        
        if won:
            player.wins += 1
        else:
            player.losses += 1
        
        return self.save(player)
    
    def get_ranking(self, limit: Optional[int] = None) -> List[Player]:
        #Retorna ranking ordenado por vitórias
        players = self.get_all()
        players.sort(reverse=True)
        
        return players[:limit] if limit else players
    
    def _parse_player_line(self, line: str) -> Optional[Player]:
        #Converte linha do arquivo em objeto Player
        try:
            parts = line.strip().split('|')
            if len(parts) != 3:
                return None
            
            name, wins, losses = parts
            return Player(
                name=name.strip(),
                wins=int(wins),
                losses=int(losses)
            )
        except Exception:
            return None
