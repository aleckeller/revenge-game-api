import requests
import json

import sportsbetanalyzer.sports_objects as sports_objects
import sportsbetanalyzer.CONSTANTS as CONSTANTS

class OddsAPI:
    def __init__(self, league: str, api_key: str):
        self.league = league
        self.api_key = api_key
    
    def get_games_with_odds(self):
        sport_key = sports_objects.get_sport_object(self.league, CONSTANTS.ODDS_API_SPORTS_KEY)
        games_with_odds = {}
        for market in CONSTANTS.ODDS_MARKETS:
            request = requests.get(CONSTANTS.ODDS_API_URL, params={
                "api_key": self.api_key,
                "sport": sport_key,
                "region": "us",
                "mkt": market,
                "oddsFormat": "american"
            })
            odds_json = json.loads(request.text)
            if not odds_json["success"]:
                print(
                    "There was a problem with the odds request:",
                    odds_json["msg"]
                )

            else:
                odds_data = odds_json["data"]
                for game in odds_data:
                    home_team = game.get("home_team")
                    if home_team:
                        home_team = home_team.lower()
                        for team in game.get("teams"):
                            if team.lower() != home_team:
                                away_team = team.lower()
                        odds = {}
                        sites = game.get("sites")
                        if self.league == CONSTANTS.NCAAB:
                            game_key = home_team
                        else:
                            game_key = home_team + away_team
                        if sites and len(sites) > 0:
                            for site in sites:
                                site_key = site.get("site_key")
                                if site_key and site_key in CONSTANTS.ODDS_SITES:
                                    site_odds = site.get("odds")
                                    if site_odds and site_odds.get(market):
                                        if games_with_odds.get(game_key):
                                            if games_with_odds[game_key]["odds"].get(site_key):
                                                old_odds_site_key = games_with_odds[game_key]["odds"][site_key]
                                                old_odds_site_key[market] = site_odds.get(market)
                                                odds[site_key] = old_odds_site_key
                                        else:
                                            odds[site_key] = {
                                                market: site_odds.get(market)
                                            }
                        games_with_odds[game_key] = {
                            CONSTANTS.TEAMS : game.get("teams"),
                            "odds": odds
                        }
        return games_with_odds