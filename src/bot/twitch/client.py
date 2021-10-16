from typing import Union
from httpx import get, post
from src.bot.twitch.handlers import handle_response


class TwitchClient:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self._oauth_token = __class__.get_oauth(client_id, client_secret)
        self.base_url = "https://api.twitch.tv/"
        self.auth_header = {
            "Client-ID": client_id,
            "Authorization": f"Bearer {self._oauth_token}",
        }

    @staticmethod
    def get_oauth(client_id: str, client_secret: str) -> str:
        """
        Obter credenciais de login para usar
        na API da Twitch
        """

        url = "https://id.twitch.tv/oauth2/token"

        params = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        }

        res = post(url, params=params)

        res_json = handle_response(res)

        return res_json["access_token"]

    def get_streams(self):
        """
        Obter informações sobre todas as streams
        """

        url = f"{self.base_url}helix/streams"

        res = get(url, headers=self.auth_header)

        res_json = handle_response(res)

        res_data = res_json.get("data")

        if res_data != []:
            return res_data

        return False

    def get_stream(self, user_id: str) -> Union[bool, dict]:
        """
        Obter informações sobre um stream
        """
        url = f"{self.base_url}helix/streams?user_id={user_id}"

        res = get(url, headers=self.auth_header)

        res_json = handle_response(res)

        res_data = res_json.get("data")

        if res_data != []:
            return res_data[0]

        return False

    def get_streamer_id(self, streamer_name: str) -> Union[bool, str]:
        """
        Obter o id de um streamer dado seu nome
        """
        url = f"{self.base_url}helix/users"

        params = {"login": streamer_name}

        res = get(url, params=params, headers=self.auth_header)

        res_json = handle_response(res)

        res_data = res_json.get("data")

        if res_data != []:
            streamer_id = res_data[0]["id"]

            return streamer_id

        return False
