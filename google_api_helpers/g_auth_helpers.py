from enum import Enum
from pathlib import Path
from typing import List, Union

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from google_api_helpers.app_config import get_g_credentials_path


class AuthScope(Enum):
    SpreadSheet = 'https://www.googleapis.com/auth/spreadsheets'
    SpreadSheetReadOnly = 'https://www.googleapis.com/auth/spreadsheets.readonly'

    Drive = 'https://www.googleapis.com/auth/drive'
    DriveFile = 'https://www.googleapis.com/auth/drive.file'
    DriveReadOnly = 'https://www.googleapis.com/auth/drive.readonly'

    Gmail = 'https://www.googleapis.com/auth/gmail'
    GmailReadOnly = 'https://www.googleapis.com/auth/gmail.readonly'


class GAuthHandler:
    def __init__(self, auth_scopes: Union[List[AuthScope], None]):
        # scope
        if not auth_scopes:
            auth_scopes = [AuthScope.SpreadSheet, AuthScope.GmailReadOnly]
        self.auth_scopes: List[str] = [auth_scope.value for auth_scope in auth_scopes]

        # credentials
        self.credential_folder_path: Path = get_g_credentials_path()
        self.credential_path: Path = Path(self.credential_folder_path,
                                          f'g_credentials.json')
        self.token_path: Path = Path(self.credential_folder_path, f'g_token.json')

        self.authorized_creds = None

    def get_g_auth(self) -> bool:
        """Return True if auth to GSheet has been authorized"""

        # check if a token has already been given
        creds = None
        # check that user has provided a credential file and saved it to the g_credentials folder
        if not Path.exists(self.credential_path):
            print(f'User need to provide a credential.json file\n'
                  f'In: {self.credential_path}\n'
                  f'README.md file')
            return False

        # check if used token exist
        if Path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(str(self.token_path), self.auth_scopes)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credential_path), self.auth_scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        else:
            # print('Valid credentials')
            self.authorized_creds = creds

        return True


if __name__ == '__main__':
    gsheet_auth = GAuthHandler(auth_scopes=[AuthScope.GmailReadOnly,
                                            AuthScope.SpreadSheet, AuthScope.SpreadSheetReadOnly])
    print(gsheet_auth.auth_scopes)
    print(gsheet_auth.auth_scopes)
    print(gsheet_auth.get_g_auth())
    print(vars(gsheet_auth))
