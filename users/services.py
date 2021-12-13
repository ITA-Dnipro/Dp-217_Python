from enrollment_assistant import settings
from enrollment_assistant.services import produce_message


def send_result(user_email, text):
    partition = {'items': [{'mail': user_email,
                            'subject': 'Enrollment assistant - Favourites',
                            'text': text}]}
    produce_message(settings.TOPIC_SEND_MAIL, partition)
    
