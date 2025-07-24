from flask_restful import Resource, reqparse
from modules.faceit import Steam, Faceit

class FaceitStats(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('steam_link', 
                        type=str, 
                        required=True, 
                        help="Steam link is required")

    @staticmethod
    def _extract_steam_id(link: str) -> str:
        try:
            steam_id = Steam(link.strip()).get_id()
            if not steam_id: 
                return ValueError("SteamID not found.")
            return steam_id
        except Exception as e: 
            raise ValueError("Invalid Link") from e
    
    @staticmethod
    def _build_response_(stats: dict) -> dict: 
        return {
            "nickname": stats['Nickname'],
            "avatar": stats["Avatar"],
            "steamid": stats["SteamID"],
            "kills": int(stats["Kills"]),
            "assists": int(stats["Assists"]),
            "deaths": int(stats["Deaths"]),
            "kd": stats["K/D"],
            "kr": stats["K/R"],
            "adr": stats["ADR"],
            "elo": int(stats['Elo']),
            "level": Faceit.calculate_lvl(int(stats['Elo']))
        }

    def post(self):
        args = self.parser.parse_args()
        try:
            steamid = self._extract_steam_id(args["steam_link"])
            stats = Faceit(steamid).get_stats(30)
            print(stats)
        except ValueError: 
            return {"error": "No player found with the given Steam link"}, 404
        except Exception as e: 
            return {"error": "Failed to retrieve FACEIT stats"}, 500
        
        return self._build_response_(stats), 200