from curl_cffi import requests
from bs4 import BeautifulSoup
import re

class Steam: 
    def __init__(self, steam_link: str = ''):
        self.steam_link = steam_link
    
    def get_id(self) -> str: 
        if "id" in self.steam_link:
            response = requests.get(self.steam_link, impersonate="chrome110")
            bs = BeautifulSoup(response.text, 'lxml') 
            scripts = bs.find_all('script')[-1].text
            return re.search(r'7656\d{13}', scripts).group()
        else: 
            return self.steam_link.split("/")[4]


class Faceit(): 
    def __init__(self, steam_link):
        self.steam_link = steam_link

    def get_profile(self) -> str: 
        response = requests.get(f"https://www.faceit.com/api/searcher/v1/players?limit=20&offset=0&game_id={self.steam_link}", 
                                impersonate="chrome110").json()
        print(response)
        for item in response["payload"]:
            userid = item["id"]
            nickname = item["nickname"]
        return userid, nickname
    
    # i6 - kills | i7 - assists | i8 - deaths | c10 - ADR | c2 - KD | c3 - KR |
    def get_stats(self):
        response = requests.get("https://www.faceit.com/api/stats/v1/stats/time/users/57224ec4-f3f6-480b-ab89-ea13b8008327/games/cs2?size=50&game_mode=5v5",
                                impersonate="chrome110").json()
        for item in response: 
            kills, assists, deaths = item['i6'], item['i7'], item['i8']
            print(f"{kills}|{assists}|{deaths}")
        
if __name__ == "__main__": 
    steam = Steam("https://steamcommunity.com/id/f1ns1ck/")
    steamid = steam.get_id()

    faceit = Faceit(steamid)
    faceit.get_stats()
