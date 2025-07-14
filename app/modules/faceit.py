from curl_cffi import requests
from bs4 import BeautifulSoup
import re, json

class Steam: 
    def __init__(self, steam_link: str = ''):
        self.steam_link = steam_link
    
    def get_id(self) -> str: 
        if "id" in self.steam_link:
            response = requests.get(self.steam_link, impersonate="chrome110")
            bs = BeautifulSoup(response.text, 'lxml') 
            scripts = bs.find_all('script')
            for item in scripts:
                if 'g_rgProfileData' in item.text:
                    return re.search(r'7656\d{13}', item.text).group()
        else: 
            return self.steam_link.split("/")[4]


class Faceit(): 
    def __init__(self, steam_link):
        self.steam_link = steam_link
        self.stats = {
            "Nickname": "",
            "Avatar": "",
            "SteamID": steam_link,
            "Elo": 0,
            "Matches": 0,
            "Kills": 0,
            "Assists": 0,
            "Deaths": 0,
            "K/D": 0,
            "K/R": 0,
            "ADR": 0
        }


    def get_profile(self) -> str: 
        response = requests.get(f"https://www.faceit.com/api/searcher/v1/players?limit=20&offset=0&game_id={self.steam_link}", 
                                impersonate="chrome110").json()
        if not response.get("payload"):
            raise ValueError("No player found with the given Steam link")
        first_player = response["payload"][0]
        self.stats["Nickname"] = first_player['nickname']
        self.stats["Avatar"] = first_player['avatar']
        return first_player["id"]
    
    # i6 - kills | i7 - assists | i8 - deaths | c10 - ADR | c2 - KD | c3 - KR |
    def get_stats(self, count: int = 0) -> json:
        userid = self.get_profile()
        response = requests.get(f"https://www.faceit.com/api/stats/v1/stats/time/users/{userid}/games/cs2?size={count}&game_mode=5v5",
                                impersonate="chrome110").json()
        matches = 0
        rounds = 0
        for item in response: 
            kills, assists, deaths = item['i6'], item['i7'], item['i8']
            self.stats['Kills'] += int(kills)
            self.stats['Assists'] += int(assists)
            self.stats['Deaths'] += int(deaths)
            self.stats["K/D"] += round(float(item["c2"]), 2)
            self.stats["ADR"] += round(float(item["c10"]), 1)
            self.stats["K/R"] += round(float(item["c3"]), 2)
            rounds += int(item['i18'].split(" / ")[0]) + int(item['i18'].split(" / ")[1])
            matches += 1
        
        self.stats['Matches'] =  matches

        for item in response:
            self.stats["Elo"] = item['elo']
            break

        if matches > 0: 
            self.stats['Kills'] = round(self.stats['Kills'] / matches)
            self.stats['Assists'] = round(self.stats['Assists'] / matches)
            self.stats['Deaths'] = round(self.stats['Deaths'] / matches)
            self.stats["K/D"] = round(self.stats["K/D"] / matches, 2)
            self.stats["K/R"] = round(self.stats["K/R"] / matches, 2)
            self.stats['ADR'] = round(self.stats['ADR'] / matches, 2)
        print(self.stats)
        return self.stats

    def calculate_lvl(self, elo):
        match elo: 
            case x if 100 <= x <= 500: 
                return "1"
            case x if 501 <= x <= 750: 
                return "2"
            case x if 751 <= x <= 900:
                return "3"
            case x if 901 <= x <= 1050:
                return "4"
            case x if 1051 <= x <= 1200: 
                return "5"
            case x if 1201 <= x <= 1350: 
                return "6"
            case x if 1351 <= x <= 1530:
                return "7"
            case x if 1531 <= x <= 1750: 
                return "8"
            case x if 1751 <= x <= 2000:
                return "9"
            case x if 2001 <= x:
                return "10"


if __name__ == "__main__": 
    steam = Steam("https://steamcommunity.com/id/daekside6666666/")
    steamid = steam.get_id()
    print(steamid, "steamid")
    fac = Faceit(steamid)
    stats = fac.get_stats(30)
    el = fac.calculate_lvl(501)

    # 523 453
