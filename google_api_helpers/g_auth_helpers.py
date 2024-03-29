import logging
from enum import Enum
from os import environ
from pathlib import Path
from typing import List, Union
from google.auth.exceptions import RefreshError

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from google_api_helpers.app_config import get_g_credentials_path
from google_api_helpers.app_config import (logging_config)

logger = logging.getLogger(f"g_auth_helpers:{Path(__file__).name}")


class AuthScope(Enum):
    SpreadSheet = 'https://www.googleapis.com/auth/spreadsheets'
    SpreadSheetReadOnly = 'https://www.googleapis.com/auth/spreadsheets.readonly'

    Drive = 'https://www.googleapis.com/auth/drive'
    DriveFile = 'https://www.googleapis.com/auth/drive.file'
    DriveReadOnly = 'https://www.googleapis.com/auth/drive.readonly'

    Gmail = 'https://www.googleapis.com/auth/gmail'
    GmailReadOnly = 'https://www.googleapis.com/auth/gmail.readonly'


class GAuthHandler:
    def __init__(self, auth_scopes: Union[List[AuthScope], None],
                 credentials_folder_path: Union[Path, str, None] = None):
        # scope
        if not auth_scopes:
            auth_scopes = [AuthScope.SpreadSheet, AuthScope.GmailReadOnly]
        self.auth_scopes: List[str] = [auth_scope.value for auth_scope in auth_scopes]

        # credentials
        if credentials_folder_path is None:
            self.credential_folder_path: Path = get_g_credentials_path()
        else:
            self.credential_folder_path: Path = Path(credentials_folder_path)
        # https://stackoverflow.com/questions/51554341/google-auth-exceptions-defaultcredentialserror
        environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(self.credential_folder_path)

        self.credential_path: Path = Path(self.credential_folder_path,
                                          'g_credentials.json')
        self.token_path: Path = Path(self.credential_folder_path,
                                     'g_token.json')

        self.authorized_creds = None

    def get_g_auth(self) -> bool:
        """Return True if auth to GSheet has been authorized"""
        # check if a token has already been given
        creds = None
        # check that user has provided a credential file and saved it to the g_credentials folder
        if not self.credential_path.is_file():
            logger.info(f'User need to provide a credential.json file. '
                        f'In: {self.credential_path}. '
                        f'README.md file')
            return False

        # check if used token exist
        if self.token_path.is_file():
            creds = Credentials.from_authorized_user_file(str(self.token_path), self.auth_scopes)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except RefreshError as ex:
                    logger.debug(f'RefreshError handled: {ex}')
                    return False
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credential_path), self.auth_scopes)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())

        # save the credentials
        self.authorized_creds = creds

        return True


if __name__ == '__main__':
    logging_config(log_file_name="g_auth_helpers.log",
                   force_local_folder=True,
                   log_level=logging.INFO)

    gsheet_auth = GAuthHandler(auth_scopes=None)
    print(gsheet_auth.auth_scopes)
    print(gsheet_auth.auth_scopes)
    print(gsheet_auth.get_g_auth())
    print(vars(gsheet_auth))
