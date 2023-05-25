import requests


def connect_and_set_session_id(user_id: str, connect_json: dict[str, any]) -> str:
    """Request solgard api for connect set, self.session_id"""

    url = f"https://api-live.thor.snowprintstudios.com/player/player2/userId/{user_id}"

    try:
        response = requests.post(url, json=connect_json)
        session_id_extracted = response.json()["eventResult"]["eventResponseData"]["userData"]["sessionId"]

        return session_id_extracted
    except:
        raise ValueError("Connexion failed")


class ApiSolgard:
    def __init__(self, user_id: str, session_id: str) -> None:
        self.user_id = user_id
        self.session_id = session_id

    def api_endpoint(self, json: dict[str, any]) -> dict[str, any]:
        if self.session_id is None:
            raise ValueError("You cant do that without session_id, connect first")

        url = f"https://api-live.thor.snowprintstudios.com/player/player2/userId/{self.user_id}/sessionId/{self.session_id}"

        try:
            response = requests.post(url, json=json)
            return response.json()
        except:
            raise ValueError("Request failed")

    def api_channel(self, json: dict[str, any]) -> dict[str, any]:
        if self.session_id is None:
            raise ValueError("You cant do that without session_id, connect first")

        url = f"https://channel-live.thor.snowprintstudios.com/events/lp/userId/{self.user_id}/sessionId/{self.session_id}"

        try:
            response = requests.post(url, json=json)
            return response.json()
        except:
            raise ValueError("Request failed")
