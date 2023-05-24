import requests


class ApiSolgard:
    def __init__(self, user_id: str, session_id: str = None) -> None:
        self.user_id = user_id
        self.session_id = session_id

    def connect_and_set_session_id(self, connect_json) -> None:
        """Request solgard api for connect set, self.session_id"""

        url = f"https://api-live.thor.snowprintstudios.com/player/player2/userId/{self.user_id}"

        try:
            response = requests.post(url, json=connect_json)
            session_id_extracted = response.json()["eventResult"]["eventResponseData"]["userData"]["sessionId"]

            # can be used for set session_id here or returned in connect_user
            self.session_id = session_id_extracted
            return session_id_extracted
        except:
            raise ValueError("Connexion failed")

    def api_endpoint(self, json):
        if self.session_id is None:
            raise ValueError("You cant do that without session_id, connect first")

        url = f"https://api-live.thor.snowprintstudios.com/player/player2/userId/{self.user_id}/sessionId/{self.session_id}"

        try:
            response = requests.post(url, json=json)
            return response.json()
        except:
            raise ValueError("Request failed")
