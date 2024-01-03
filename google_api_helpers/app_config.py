"""Mainly Path and env functions that are used globally in the app"""
import logging
import platform
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

logger = logging.getLogger(f"g_mail_helpers:{Path(__file__).name}")


def get_project_root_path() -> Path:
    root_dir = Path(__file__).parent.parent
    # print(root_dir)
    return root_dir


def load_env_variables():
    load_dotenv()


def get_root_full_path() -> Path:
    """Return the app root folder path"""
    app_root_path: Path = Path(__file__).parent
    return app_root_path


def get_g_credentials_path() -> Path:
    """Return the path to the Google credentials folder and create the folder if it doesn't exist"""
    app_root_path: Path = get_root_full_path()
    credential_path: Path = Path(app_root_path, "g_credentials")

    if not credential_path.exists():
        credential_path.mkdir(parents=False,  # uses parent False as it shouldn't have to create any parent folders
                              exist_ok=True)
    return credential_path


def logging_config(log_file_name: Optional[str] = None,
                   force_local_folder: bool = False,
                   project_name: Optional[str] = None,
                   log_level: int = logging.DEBUG):
    """Create a basic logging file

    Args:
        log_file_name (Optional[str], optional): a file name ending with '.log' which will be stored in the log folder. Defaults to None.
        force_local_folder (bool=False): ignore system parameter and save logs locals within the downloads folder
        project_name (Optional[str]=None): names the logging folder, if ignored, uses the app name
        log_level (int=logging.DEBUG): the log level

    """
    if not project_name:
        project_name = get_project_root_path().name

    # Handles folder to log into
    if force_local_folder:
        logging_folder = Path(get_project_root_path(), project_name, "downloads")
        logging_folder.mkdir(parents=True, exist_ok=True)
    else:
        if platform.system() == 'Linux':
            logging_folder = Path('/var', "log", "my_apps", "python", project_name, )
            logging_folder.mkdir(parents=True, exist_ok=True)
        else:
            logging_folder = Path(get_project_root_path(), project_name, "downloads")
            logging_folder.mkdir(parents=True, exist_ok=True)
    # handles log file name
    if log_file_name:
        logging_file_path = Path(logging_folder, log_file_name)
    else:
        logging_file_path = Path(logging_folder, f'{project_name}.log')

    # Configure the root logger
    logging.basicConfig(
        filename=logging_file_path,  # Global log file name
        level=log_level,  # Global log level
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


if __name__ == '__main__':
    print(get_root_full_path())
    print(get_g_credentials_path())
    load_dotenv()
