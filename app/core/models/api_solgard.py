from typing import Any
import requests
from requests import RequestException


def connect_and_set_session_id(user_id: str, connect_json: dict[str, Any]) -> str:
    """
    Sends a POST request to the Solgard API to connect and set the session_id.

    Parameters
    ----------
    user_id : str
        The ID of the user.
    connect_json : dict[str, Any]
        JSON data to be sent in the POST request.

    Returns
    -------
    str
        The session ID extracted from the response.

    Raises
    ------
    ValueError
        If the connection failed.
    """

    url = f"https://api-live.thor.snowprintstudios.com/player/player2/userId/{user_id}"

    try:
        response = requests.post(url, json=connect_json, timeout=5)
        session_id_extracted = response.json()["eventResult"]["eventResponseData"]["userData"]["sessionId"]

        return session_id_extracted
    except RequestException:
        raise ValueError("Connexion failed")


class ApiSolgard:
    """
    Class to handle interactions with the Solgard API.

    Attributes
    ----------
    user_id : str
        The ID of the user.
    session_id : str
        The session ID of the user.

    Raises
    ------
    ValueError
        If no session_id is provided.
    """

    __slots__ = ["user_id", "session_id"]

    def __init__(self, user_id: str, session_id: str) -> None:
        """
        Initialize an instance of ApiSolgard.

        Parameters
        ----------
        user_id : str
            The ID of the user.
        session_id : str
            The session ID of the user.
        """
        self.user_id = user_id
        self.session_id = session_id

    def api_endpoint(self, json: dict[str, Any]) -> dict[str, Any]:
        """
        Sends a POST request to the Solgard API endpoint.

        Parameters
        ----------
        json : dict[str, Any]
            JSON data to be sent in the POST request.

        Returns
        -------
        dict[str, Any]
            The JSON response from the API.

        Raises
        ------
        ValueError
            If the request failed.
        """
        if self.session_id is None:
            raise ValueError("You cant do that without session_id, connect first")

        url = f"https://api-live.thor.snowprintstudios.com/player/player2/userId/{self.user_id}/sessionId/{self.session_id}"

        try:
            response = requests.post(url, json=json, timeout=5)
            return response.json()
        except RequestException as e:
            raise ValueError("Request failed") from e

    def api_channel(self, json: dict[str, Any]) -> dict[str, Any]:
        """
        Sends a POST request to the Solgard API channel.

        Parameters
        ----------
        json : dict[str, Any]
            JSON data to be sent in the POST request.

        Returns
        -------
        dict[str, Any]
            The JSON response from the API.

        Raises
        ------
        ValueError
            If the request failed.
        """
        if self.session_id is None:
            raise ValueError("You cant do that without session_id, connect first")

        url = f"https://channel-live.thor.snowprintstudios.com/events/lp/userId/{self.user_id}/sessionId/{self.session_id}"

        try:
            response = requests.post(url, json=json, timeout=5)
            return response.json()
        except RequestException as e:
            raise ValueError("Request failed") from e
