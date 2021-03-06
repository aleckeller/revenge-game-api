from typing import List
from sportsbetanalyzer.Player import Player
from sportsbetanalyzer.Team import Team
from json_logic import jsonLogic
from datetime import datetime
from sportsbetanalyzer import CONSTANTS
import utils
from sportsbetanalyzer.Game import Game

class RevengeGame(Game):
    def __init__(self, league: str, date_of_game: datetime, home_team: Team, away_team: Team, metrics: List[str], rules: List[object], odds: object, revenge_game_players: List[Player]):
        super().__init__(league, date_of_game, home_team, away_team, metrics, rules, odds)
        self.revenge_game_players = revenge_game_players
    
    def to_dictionary(self, include_score=True):
        game_dict = super().to_dictionary(False)
        if hasattr(self, "revenge_game_players"):
            json_revenge_players = []
            for revenge_game_player in self.revenge_game_players:
                json_revenge_players.append(revenge_game_player.to_dictionary())
            game_dict["revenge_game_players"] = json_revenge_players
        return game_dict