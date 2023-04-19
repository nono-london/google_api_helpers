"""https://skillshats.com/blogs/send-and-read-emails-with-gmail-api/"""
import base64
import email
from datetime import datetime, timedelta
from typing import (Optional, List, Dict)
from typing import Union

from googleapiclient import discovery
from googleapiclient.discovery import Resource
from googleapiclient.errors import HttpError

from google_api_helpers.g_auth_helpers import (GAuthHandler, AuthScope)


class GMailHandler(GAuthHandler):
    def __init__(self, auth_scopes: Union[List[AuthScope], None] = None,
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

    def get_message_ids(self, user_id: Optional[str] = None,
                        date_from: Union[str, datetime, None] = None,
                        date_to: Union[str, datetime, None] = None,
                        ):
        """ date_from: needs to be formatted as %Y/%m/%d, defaults to last year if None
            date_to: needs to be formatted as %Y/%m/%d
        """
        if date_from is None:
            date_from = (datetime.now() - timedelta(days=365)).strftime("%Y/%m/%d")
        if user_id is None:
            user_id = self.gmail_user_id
        if isinstance(date_from, datetime):
            date_from = date_from.strftime("%Y/%m/%d")
        if isinstance(date_from, datetime):
            date_to = date_to.strftime("%Y/%m/%d")

        after = f" after:{date_from}" if date_from else ""
        before = f" before:{date_to}" if date_to else ""
        query: str = f"{after}{before}".strip()

        results: list = []
        try:
            self._init_gmail_service()
            message_ids = self.gmail_service.users().messages().list(userId=user_id, q=query).execute()
            if message_ids and message_ids.get("messages"):
                results.extend(message_ids['messages'])

            while 'nextPageToken' in message_ids:

                page_token = message_ids['nextPageToken']
                message_ids = self.gmail_service.users().messages().list(userId=user_id, pageToken=page_token).execute()
                if message_ids and message_ids.get("messages"):
                    results.extend(message_ids['messages'])

        except Exception as error:
            print('An error occurred: %s' % error)

        return results

    def get_message(self, msg_id: str, user_id: Optional[str] = None):
        if user_id is None:
            user_id = self.gmail_user_id
        try:
            self._init_gmail_service()
            messages = self.gmail_service.users().messages().get(userId=user_id, id=msg_id, format='metadata').execute()
            return messages
        except Exception as error:
            print('An error occurred: %s' % error)

    def get_mime_message(self, msg_id: str,
                         user_id: Optional[str] = None, ):

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

    def get_messages_from(self, sender_email: str,
                          date_from: Union[str, datetime, None] = None,
                          date_to: Union[str, datetime, None] = None,
                          user_id: Optional[str] = None, ) -> Union[None, List[Dict]]:
        if user_id is None:
            user_id = self.gmail_user_id
        """ date_from: needs to be formatted as %Y/%m/%d
            date_to: needs to be formatted as %Y/%m/%d

        """

        if isinstance(date_from, datetime):
            date_from = date_from.strftime("%Y/%m/%d")
        if isinstance(date_from, datetime):
            date_to = date_to.strftime("%Y/%m/%d")
        after = f" after:{date_from}" if date_from else ""
        before = f" before:{date_to}" if date_to else ""

        query: str = f"from:{sender_email}{after}{before}".strip()
        page_token = None
        results = []
        try:
            self._init_gmail_service()
            message_ids = self.gmail_service.users().messages().list(userId=user_id, q=query,
                                                                     pageToken=page_token).execute()
            if message_ids and message_ids.get("messages"):
                results.extend(message_ids['messages'])

            while 'nextPageToken' in message_ids:

                page_token = message_ids['nextPageToken']
                message_ids = self.gmail_service.users().messages().list(userId=user_id, q=query,
                                                                         pageToken=page_token).execute()
                if message_ids and message_ids.get("messages"):
                    results.extend(message_ids['messages'])

        except Exception as error:
            print('An error occurred: %s' % error)

        return results

    def query_messages(self, query: str,
                       subject_body: Optional[str] = None,
                       date_from: Union[str, datetime, None] = None,
                       date_to: Union[str, datetime, None] = None,
                       user_id: Optional[str] = None, ) -> Union[None, List[Dict]]:
        if user_id is None:
            user_id = self.gmail_user_id
        """ date_from: needs to be formatted as %Y/%m/%d
            date_to: needs to be formatted as %Y/%m/%d
            subject_body: whether to search subject only, body only or both is equal to None

        """

        if isinstance(date_from, datetime):
            date_from = date_from.strftime("%Y/%m/%d")
        if isinstance(date_from, datetime):
            date_to = date_to.strftime("%Y/%m/%d")
        after = f" after:{date_from}" if date_from else ""
        before = f" before:{date_to}" if date_to else ""
        if subject_body is None:
            query_in = ""
        elif subject_body.lower() == 'subject':
            query_in = " subject:"
        elif subject_body.lower() == 'body':
            query_in = " in:body "
        else:
            query_in = ""

        query: str = f"{after}{before}{query_in}{query}".strip()
        page_token = None
        results: list = []

        try:
            self._init_gmail_service()
            message_ids = self.gmail_service.users().messages().list(userId=user_id, q=query,
                                                                     pageToken=page_token).execute()

            if message_ids and message_ids.get("messages"):
                results.extend(message_ids['messages'])

            while 'nextPageToken' in message_ids:

                page_token = message_ids['nextPageToken']
                message_ids = self.gmail_service.users().messages().list(userId=user_id, q=query,
                                                                         pageToken=page_token).execute()
                if message_ids and message_ids.get("messages"):
                    results.extend(message_ids['messages'])

        except Exception as error:
            print('An error occurred: %s' % error)

        return results


if __name__ == '__main__':
    gmail = GMailHandler(auth_scopes=None,
                         gmail_user_id=None)
    my_result = gmail.get_message_ids(user_id=None)

    # print(my_result)
    my_result = gmail.get_message(msg_id="1879a4baf23a4ba3")
    # print(my_result)
    my_result = gmail.get_mime_message(msg_id="1879a4baf23a4ba3")

    my_result = gmail.get_messages_from(sender_email="abouttrading@substack.com",
                                        date_from=datetime(2021, 4, 1),
                                        user_id=None)
    print(my_result)
    print(len(my_result))

    my_result = gmail.query_messages(query="trading",
                                     # date_from=datetime(2021, 4, 1),
                                     user_id=None)
