from curl_cffi import requests
from bs4 import BeautifulSoup
import re
from dataclasses import dataclass


class Steam: 
    def __init__(self, steam_link: str) -> None:
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

@dataclass
class FaceitData:
    nickname: str = ""
    avatar: str = ""
    steam_id: str = ""
    elo: int = 0
    matches: int = 0
    kills: int = 0
    assists: int = 0
    deaths: int = 0
    kd : float = 0.0
    kr: float = 0.0
    adr: float = 0.0

class Faceit(): 
    def __init__(self, steam_link) -> None:
        self.steam_link = steam_link
        self.stats = FaceitData(steam_id=steam_link)


    def get_profile(self) -> str: 
        response = requests.get(f"https://www.faceit.com/api/searcher/v1/players?limit=20&offset=0&game_id={self.steam_link}", 
                                impersonate="chrome110").json()
        if not response.get("payload"):
            raise ValueError("No player found with the given Steam link")
        first_player = response["payload"][0]
        self.stats.nickname = first_player['nickname']
        self.stats.avatar = first_player['avatar']
        return first_player["id"]
    
    def get_stats(self, count: int = 30) -> dict:
        userid = self.get_profile()
        response = requests.get(f"https://www.faceit.com/api/stats/v1/stats/time/users/{userid}/games/cs2?size={count}&game_mode=5v5",
                                impersonate="chrome110").json()
        matches = 0
        for item in response: 
            kills, assists, deaths = item['i6'], item['i7'], item['i8']
            self.stats.kills += int(kills)
            self.stats.assists += int(assists)
            self.stats.deaths += int(deaths)
            self.stats.kd += round(float(item["c2"]), 2)
            self.stats.adr += round(float(item["c10"]), 1)
            self.stats.kr += round(float(item["c3"]), 2)
            matches += 1
        
        self.stats.matches =  matches

        for item in response:
            self.stats.elo = item['elo']
            break

        if matches > 0: 
            self.stats.kills = round(self.stats.kills / matches)
            self.stats.assists = round(self.stats.assists / matches)
            self.stats.deaths = round(self.stats.deaths / matches)
            self.stats.kd = round(self.stats.kd / matches, 2)
            self.stats.kr = round(self.stats.kr / matches, 2)
            self.stats.adr = round(self.stats.adr / matches, 2)
        return self.stats

    def calculate_lvl(elo) -> str:
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
    steam = Steam()
    steamid = steam.get_id()
    print(steamid, "steamid")
    fac = Faceit(steamid)
    stats = fac.get_stats(30)
    el = fac.calculate_lvl(501)