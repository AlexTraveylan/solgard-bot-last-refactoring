from app.core.models.connect_user import ConnectUser


def test_connection():
    user = ConnectUser()
    user.connect_and_get_new_session_id()

    assert user.user_id is not None
    assert user.session_id is not None
