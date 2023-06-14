from typing import Any
import requests
from requests import RequestException


def connect_and_set_session_id(user_id: str, connect_json: dict[str, Any]) -> str:
    """Request solgard api for connect set, self.session_id"""

    url = f"https://api-live.thor.snowprintstudios.com/player/player2/userId/{user_id}"

    try:
        response = requests.post(url, json=connect_json, timeout=5)
        session_id_extracted = response.json()["eventResult"]["eventResponseData"]["userData"]["sessionId"]

        return session_id_extracted
    except RequestException:
        raise ValueError("Connexion failed")


class ApiSolgard:
    def __init__(self, user_id: str, session_id: str) -> None:
        self.user_id = user_id
        self.session_id = session_id

    def api_endpoint(self, json: dict[str, Any]) -> dict[str, Any]:
        if self.session_id is None:
            raise ValueError("You cant do that without session_id, connect first")

        url = f"https://api-live.thor.snowprintstudios.com/player/player2/userId/{self.user_id}/sessionId/{self.session_id}"

        try:
            response = requests.post(url, json=json, timeout=5)
            return response.json()
        except RequestException as e:
            raise ValueError("Request failed") from e

    def api_channel(self, json: dict[str, Any]) -> dict[str, Any]:
        if self.session_id is None:
            raise ValueError("You cant do that without session_id, connect first")

        url = f"https://channel-live.thor.snowprintstudios.com/events/lp/userId/{self.user_id}/sessionId/{self.session_id}"

        try:
            response = requests.post(url, json=json, timeout=5)
            return response.json()
        except RequestException as e:
            raise ValueError("Request failed") from e
