from flask_restful import Resource, reqparse
from modules.faceit import Steam, Faceit

class FaceitStats(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('steam_link', type=str, required=True, help="Steam link is required")
        args = parser.parse_args()

        steam_link = args['steam_link'].strip()
        steamid = Steam(steam_link).get_id()
        faceit = Faceit(steamid)
        stats = faceit.get_stats(30)

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
            "level": faceit.calculate_lvl(int(stats['Elo']))
        }, 200