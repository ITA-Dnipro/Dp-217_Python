"""
Email backend that writes messages to users for changing their passwords.
"""
import json
import requests

from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings


class EmailBackend(BaseEmailBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def send_messages(self, email_messages):
        response = []
        if not email_messages:
            return
        for message in email_messages:
            for recipient in message.to:
                user_mail = recipient
                subject = str(message.subject)
                text = str(message.body)
                url = settings.MAILING_SEND_URL
                data = {'mail': user_mail, 'subject': subject, 'text': text}
                data_json = json.dumps(data)
                response.append(requests.post(url, data=data_json))
            return response
