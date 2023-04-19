from google_api_helpers.g_auth_helpers import (GAuthHandler,
                                               AuthScope)


def test_valid_connection():
    gsheet_auth = GAuthHandler(auth_scopes=[AuthScope.SpreadSheet])

    result = gsheet_auth.get_g_auth()
    assert result is True


if __name__ == '__main__':
    test_valid_connection()
