"""https://skillshats.com/blogs/send-and-read-emails-with-gmail-api/"""
import base64
import email
import os
from typing import (Optional, List)
from typing import Union

from googleapiclient import discovery
from googleapiclient.discovery import Resource
from googleapiclient.errors import HttpError

from google_api_helpers.app_config import load_env_variables
from google_api_helpers.g_auth_helpers import (GAuthHandler, AuthScope)


class GMailHandler(GAuthHandler):
    def __init__(self, auth_scopes: List[AuthScope],
                 gmail_user_id: Optional[str] = None):
        super().__init__(auth_scopes)

        # in case of delegate user, otherwise only manage email that has had auth
        self.gmail_user_id = "me" if gmail_user_id is None else gmail_user_id

        # get authorization
        self.get_g_auth()
        # if None load from .env variables

        self.gmail_service: Union[Resource, None] = None

    def _init_gmail_service(self):
        if self.gmail_service is None:
            self.gmail_service = discovery.build('gmail', 'v1', credentials=self.authorized_creds)

    def read_emails(self):
        if not any(scope.value in self.auth_scopes for scope in [AuthScope.Gmail, AuthScope.GmailReadOnly]):
            print(f"{AuthScope.Gmail.value} or {AuthScope.GmailReadOnly.value} not in auth. scopes:\n"
                  f"{self.auth_scopes}")
            return None

        try:
            # Call the Gmail API
            self._init_gmail_service()
            results = self.gmail_service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])

            if not labels:
                print('No labels found.')
                return
            print('Labels:')
            for label in labels:
                print(label['name'])

        except HttpError as error:
            print(f'An error occurred: {error}')

    def get_messages(self, user_id: Optional[str] = None):
        if user_id is None:
            user_id = self.gmail_user_id
        try:
            self._init_gmail_service()
            messages = self.gmail_service.users().messages().list(userId=user_id).execute()
            return messages
        except Exception as error:
            print('An error occurred: %s' % error)

    def get_message(self, msg_id: str, user_id: Optional[str] = None):
        if user_id is None:
            user_id = self.gmail_user_id
        try:
            self._init_gmail_service()
            messages = self.gmail_service.users().messages().get(userId=user_id, id=msg_id, format='metadata').execute()
            return messages
        except Exception as error:
            print('An error occurred: %s' % error)

    def get_mime_message(self, msg_id:str, user_id: Optional[str] = None, ):
        if user_id is None:
            user_id = self.gmail_user_id
        try:
            self._init_gmail_service()
            message = self.gmail_service.users().messages().get(userId=user_id, id=msg_id,
                                                                format='raw').execute()
            print('Message snippet: %s' % message['snippet'])
            msg_str = base64.urlsafe_b64decode(message['raw'].encode("utf-8")).decode("utf-8")
            mime_msg = email.message_from_string(msg_str)

            return mime_msg
        except Exception as error:
            print('An error occurred: %s' % error)


if __name__ == '__main__':
    gmail = GMailHandler(auth_scopes=[AuthScope.GmailReadOnly,
                                      # AuthScope.Gmail
                                      ],
                         gmail_user_id=None)
    my_result = gmail.get_messages(user_id=None)
    print(my_result)
