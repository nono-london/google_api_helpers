from typing import Union
from datetime import datetime, timedelta
from google_api_helpers.g_mail_helpers import GMailHandler,GEmail

messages: Union[list, None] = None


def test_get_msg_ids():
    global messages
    gmail = GMailHandler()
    messages = gmail.get_message_ids(date_from=datetime.utcnow()-timedelta(days=15))
    assert len(messages) > 0


def test_read_message():
    global messages
    test_get_msg_ids()
    print(messages)
    gmail = GMailHandler()
    message:GEmail = gmail.read_message(msg_id=messages[0].get('id'))
    assert len(message.body_text) > 0 and len(message.body_html) > 0


def test_read_message_metadata():
    global messages
    test_get_msg_ids()

    gmail = GMailHandler()
    message = gmail.get_message_metadata(msg_id=messages[0].get('id'))
    assert len(message) > 0


if __name__ == '__main__':
    test_get_msg_ids()
    test_read_message()
    test_read_message()
