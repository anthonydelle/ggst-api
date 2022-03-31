import msgpack
import requests
import logging

from typing import Final, List

PLAYSTATION: Final = 1
PC: Final = 3

class API:
    def __init__(self) -> None:
        self.host = "https://ggst-game.guiltygear.com"
        self.token = None

    def request(self, endpoint: str, body: List):
        headers = {'User-Agent': 'Steam', 'Content-Type': "application/x-www-form-urlencoded"}
        url: str = self.host + endpoint 
        messagePackData = msgpack.packb(body).hex()

        try:
            res = requests.post(url, data={'data': messagePackData}, headers=headers)
        except ConnectionError as e:
            logging.exception(f"An error as occured: {e}")
            return
        
        return res.content

    def login(self, steamID: str, steamIDHex: str, platform: str, version: str = "0.0.1"):
        platformID: int = 0

        if(platform.lower() == "playstation"):
            platformID = PLAYSTATION
        elif (platform.lower() == "pc"):
            platformID = PC
        else:
            logging.warning("Platform not recognized. The platform should be either 'pc' or 'playstation'.")
            return

        data = [
            [
                "",
                "",
                6,
                version,
                platformID
            ],
            [
                1,
                steamID,
                steamIDHex,
                256,
                ""
            ]
        ]

        bytesResponse = self.request("/api/user/login", data)
        res = msgpack.unpackb(bytesResponse)
        return res