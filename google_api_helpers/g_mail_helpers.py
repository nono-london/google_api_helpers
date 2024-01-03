"""https://skillshats.com/blogs/send-and-read-emails-with-gmail-api/"""
import base64
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import (Optional, List, Dict)
from typing import Union
from google_api_helpers.app_config import logging_config
from googleapiclient import discovery
from googleapiclient.discovery import Resource
from googleapiclient.errors import HttpError

from google_api_helpers.g_auth_helpers import (GAuthHandler, AuthScope)

logger = logging.getLogger(f"g_mail_helpers:{Path(__file__).name}")


class GEmail:
    def __init__(self):
        self.payload: Union[None, dict] = None
        self.subject: Union[None, str] = None
        self.sender: Union[None, str] = None
        self.received_date: Union[None, datetime, str] = None
        self.body_text: Union[None, str] = None
        self.body_html: Union[None, str] = None

    def set_received_date(self, date_as_g_string):
        try:
            self.received_date = datetime.strptime(date_as_g_string.replace(" (UTC)", ""),
                                                   "%a, %d %b %Y %H:%M:%S %z")
        except ValueError as ex:
            logger.info(f'Can not convert gmail date: {date_as_g_string}, '
                        f'Error: {ex}')
            self.received_date = date_as_g_string


class GMailHandler(GAuthHandler):
    def __init__(self, auth_scopes: Union[List[AuthScope], None] = None,
                 gmail_user_id: Optional[str] = None,
                 credentials_folder_path: Union[Path, str, None] = None):

        super().__init__(auth_scopes, credentials_folder_path)

        # in case of delegate user, otherwise only manage email that has had auth
        self.gmail_user_id = "me" if gmail_user_id is None else gmail_user_id

        # get authorization
        self.get_g_auth()
        # if None load from .env variables

        self.gmail_service: Union[Resource, None] = None

    def _init_gmail_service(self):
        if self.gmail_service is None:
            self.gmail_service = discovery.build('gmail', 'v1', credentials=self.authorized_creds)

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

        except Exception as ex:
            logger.error(f'Error with google_api_helpers'
                         f' with get_message_ids {ex.__class__.__name__}'
                         f'Error: {ex}')

        return results

    def get_message_metadata(self, msg_id: str, user_id: Optional[str] = None) -> Dict:
        if user_id is None:
            user_id = self.gmail_user_id
        try:
            self._init_gmail_service()
            message: dict = self.gmail_service.users().messages().get(userId=user_id, id=msg_id,
                                                                      format='metadata').execute()

            return message
        except Exception as ex:
            logger.error(f'Error with google_api_helpers. '
                         f'With get_message_metadata: {ex.__class__.__name__}. '
                         f'Error is: {ex}')

    def read_message(self, msg_id: str, user_id: Optional[str] = None) -> Union[GEmail, None]:
        if user_id is None:
            user_id = self.gmail_user_id
        try:
            self._init_gmail_service()
            message: dict = self.gmail_service.users().messages().get(userId=user_id, id=msg_id,
                                                                      format='full').execute()
            gmail_email = GEmail()

            # Parse the message payload
            gmail_email.payload = message['payload']
            headers = gmail_email.payload['headers']
            gmail_email.subject = next((header['value'] for header in headers if header['name'] == 'Subject'), '')
            gmail_email.sender = next((header['value'] for header in headers if header['name'] == 'From'), '')
            date_as_g_string = next((header['value'] for header in headers if header['name'] == 'Date'), '')
            gmail_email.set_received_date(date_as_g_string=date_as_g_string)

            # Decode the message body
            text_body = ''
            html_body = ''
            if 'parts' in gmail_email.payload:
                parts = gmail_email.payload['parts']
                for part in parts:
                    if part['mimeType'] == 'text/plain':
                        text_body += part['body']['data']
                    if part['mimeType'] == 'text/html':
                        html_body += part['body']['data']
                if html_body != '':
                    gmail_email.body_html = base64.urlsafe_b64decode(html_body).decode()
            else:
                text_body = gmail_email.payload['body']['data']
                gmail_email.body_html = None

            gmail_email.body_text = base64.urlsafe_b64decode(text_body).decode()

            return gmail_email

        except HttpError as ex:
            logger.info(f'Error with google_api_helpers. '
                        f'With read_message: {ex.__class__.__name__}. '
                        f'Error is: {ex}')
            return None

    def get_messages_ids_from(self, sender_email: str,
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

        except HttpError as ex:
            logger.error(f'Error with google_api_helpers. '
                         f'With get_messages_ids_from: {ex.__class__.__name__}. '
                         f'Error is: {ex}')
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

        except Exception as ex:
            logger.error(f'Error with google_api_helpers. '
                         f'With query_messages: {ex.__class__.__name__}. '
                         f'Error is: {ex}')
        return results


if __name__ == '__main__':
    logging_config(log_file_name="g_mail_helpers.log",
                   force_local_folder=True,
                   log_level=logging.INFO)
    gmail = GMailHandler(auth_scopes=None,
                         gmail_user_id=None)

    my_result = gmail.read_message(msg_id="")
    if my_result.body_html is None:
        print(my_result.body_text)

    print(my_result.body_html)
    # print(my_result.body_text)
    print(my_result.sender)
    print(my_result.received_date)
