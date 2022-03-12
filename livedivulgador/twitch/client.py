from typing import Union
from time import sleep
from httpx import get, post
from logging import getLogger
from livedivulgador.helpers.slice import slice_queue
from livedivulgador.twitch.handlers import handle_response


logger = getLogger(__name__)


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

    def get_random_streams(self):
        """
        Obter informações sobre todos os streams
        """

        url = f"{self.base_url}helix/streams"

        res = get(url, headers=self.auth_header)

        res_json = handle_response(res)

        res_data = res_json.get("data")

        if res_data != []:
            return res_data

        return False

    def get_streams(self, user_ids: list[str]) -> list[dict]:
        """
        Obter informações sobre streams de vários usuários
        """
        tries = 5
        streams = []
        user_ids_generator = slice_queue(user_ids)

        for user_ids_slice in user_ids_generator:
            query = "&user_id=".join(user_ids_slice)
            url = f"{self.base_url}helix/streams/?user_id={query}"

            for _ in range(tries):
                try:
                    res = get(url, headers=self.auth_header)
                except Exception as e:
                    err = e
                    logger.error(f"{err}, retrying within a minute")
                    sleep(60)
                    continue
                else:
                    break
            else:
                raise err

            res_json = handle_response(res)

            res_data = res_json.get("data")

            streams.append(res_data)

        flattened_streams = [item for sublist in streams for item in sublist]

        return flattened_streams

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
