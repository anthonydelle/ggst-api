import msgpack
import requests
import logging
import json

from typing import Dict, List, Optional, Union, Any
from .constants import PLAYSTATION, PC, VERSION, CHARACTERS


class API:
    def __init__(self) -> None:
        self.host: str = "https://ggst-game.guiltygear.com"
        self.token: Optional[str] = None
        self.currentUser: Optional[str] = None
        self.platform: Optional[int] = None

    def _get_platform(self, platform: str) -> int:
        if platform.lower() == "playstation":
            return PLAYSTATION
        elif platform.lower() == "pc":
            return PC
        else:
            raise ValueError("Platform not recognized. The platform should be either 'pc' or 'playstation'.")

    def _get_character(self, character: str) -> int:
        if character in CHARACTERS.keys():
            return CHARACTERS[character]
        else:
            raise ValueError("The character was not recognized.")

    def _request(self, endpoint: str, body: List) -> Union[List, None]:
        headers = {
            "User-Agent": "Steam",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        }
        url: str = self.host + endpoint
        messagePackData = msgpack.packb(body).hex()

        try:
            res = requests.post(url, data={"data": messagePackData}, headers=headers)
        except ConnectionError as e:
            logging.exception(f"An error as occured: {e}")
            return None

        unpackedRes: List = msgpack.unpackb(res.content)

        return unpackedRes

    def login(self, steamID: str, steamIDHex: str, platform: str) -> Union[List, None]:
        platformID: int = self._get_platform(platform)

        data: List = [
            ["", "", 6, VERSION, platformID],
            [1, steamID, steamIDHex, 256, ""],
        ]

        res: Any = self._request("/api/user/login", data)
        self.token = res[0][0]
        self.currentUser = res[1][1][0]
        self.platform = platformID

        return res

    def get_rcode(self, playerID: str, platform: str = "pc") -> Dict:
        platformID: int = self._get_platform(platform)

        data: List = [
            [
                self.currentUser if self.currentUser != None else "",
                self.token if self.token != None else "",
                6,
                VERSION,
                self.platform if self.platform != None else platformID,
            ],
            [playerID, 7, -1, -1, -1, -1],
        ]

        res: Any = self._request("/api/statistics/get", data)

        return json.loads(res[1][1])

    def get_matches_stats(self, playerID: str, character: str = "All", platform: str = "pc") -> Dict:
        platformID: int = self._get_platform(platform)
        characterID: int = self._get_character(character)

        data: List = [
            [
                self.currentUser if self.currentUser != None else "",
                self.token if self.token != None else "",
                6,
                VERSION,
                self.platform if self.platform != None else platformID,
            ],
            [playerID, 1, 1, characterID, -1, -1],  # Character ID
        ]

        res: Any = self._request("/api/statistics/get", data)
        return json.loads(res[1][1])

    def get_skills_stats(self, playerID: str, character: str = "All", platform: str = "pc") -> Dict:
        platformID: int = self._get_platform(platform)
        characterID: int = self._get_character(character)

        data: List = [
            [
                self.currentUser if self.currentUser != None else "",
                self.token if self.token != None else "",
                6,
                VERSION,
                self.platform if self.platform != None else platformID,
            ],
            [playerID, 2, 1, characterID, -1, -1],  # Character ID
        ]

        res: Any = self._request("/api/statistics/get", data)
        return json.loads(res[1][1])
