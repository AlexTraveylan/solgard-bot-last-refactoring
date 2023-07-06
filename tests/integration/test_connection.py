import os
from dotenv import load_dotenv
from app.core.models.connect_user import ConnectUser


def test_connection():
    load_dotenv()
    KEY = os.getenv("KEY")
    CONFIG_ENCRYPTED = os.getenv("CONFIG_ENCRYPTED")
    if KEY is None:
        raise ValueError("KEY not found")
    if CONFIG_ENCRYPTED is None:
        raise ValueError("CONFIG_ENCRYPTED not found")

    user = ConnectUser(CONFIG_ENCRYPTED, KEY)
    user.connect_and_get_new_session_id()
    assert user.session_id is not None
