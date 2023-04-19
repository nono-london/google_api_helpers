from os import environ

from google_api_helpers.app_config import (get_g_credentials_path, load_env_variables, get_root_full_path)


def test_dot_env():
    load_env_variables()
    gsheet_id = environ.get('G_SHEET_ID')
    print(gsheet_id)
    assert gsheet_id is not None


def test_root_path():
    root_path = get_root_full_path()
    assert root_path.exists()


def test_credentials_folder():
    cred_folder = get_g_credentials_path()
    assert cred_folder.exists()


if __name__ == '__main__':
    test_credentials_folder()
    test_root_path()
    test_dot_env()
