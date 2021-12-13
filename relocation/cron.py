from enrollment_assistant.services import produce_message
from users.models import CustomUser
from universearch.models import University


def remind_about_housing():
    partition = {
        'items': []
    }
    for user in CustomUser.objects.filter(is_interested_in_relocation=True):
        text = f'''Шановний(-вна) {user.first_name}! Ви
            підписані на новини щодо релокації. Нагадуємо, що
            на сайті Enrollment assistant ви можете знайти
            інформацію та контактні дані будь-якого житла у
            місті університетів: {[uni.name for uni in University.objects.filter(id__in=user.favourites)]}.\n\n
            Щоб відписатись від таких листів, перейдіть у свій
            профіль на сайті та виберіть відповідну опцію.'''
        partition['items'].append({'mail': user.email,
                                   'subject': 'Enrollment assistant - Relocation',
                                   'text': text})
    produce_message(topic='send_mail', partition=partition)
