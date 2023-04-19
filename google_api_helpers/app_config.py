"""Mainly Path and env functions that are used globally in the app"""
from pathlib import Path

from dotenv import load_dotenv


def load_env_variables():
    env_path: Path = Path(get_root_full_path(), ".env")
    if not env_path:
        print(f"No env file found for path: {env_path}")
        raise Exception(f".env file not found")
    load_dotenv(env_path)


def get_root_full_path() -> Path:
    """Return the app root folder path"""
    app_root_path: Path = Path().cwd().parent
    return app_root_path


def get_g_credentials_path() -> Path:
    """Return the path to the Google credentials folder and create the folder if it doesn't exist"""
    app_root_path: Path = get_root_full_path()
    credential_path: Path = Path(app_root_path, app_root_path.name, "g_credentials")
    if not (credential_path.exists()):
        credential_path.mkdir(parents=False,  # uses parent False as it shouldn't have to create any parent folders
                              exist_ok=True)
    return credential_path


if __name__ == '__main__':
    print(get_root_full_path())
    print(get_g_credentials_path())
    load_dotenv()
