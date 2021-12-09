from enrollment_assistant.services import produce_message
from users.models import CustomUser


def remind_about_housing():
    partition = {
        'items': []
    }
    for user in CustomUser.objects.filter(is_relocating=True):
        if user.is_interested_in_relocation:
            partition['items'].append({'mail': user.email,
                                       'subject': 'Enrollment assistant - Relocation',
                                       'text': 'Не забудьте що вам нема де жити!'})
    produce_message(topic='send_email', partition=partition)
