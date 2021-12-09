import datetime
from users.models import CustomUser


def remove_users():
    now = datetime.datetime.now()
    CustomUser.objects.filter(deletion_request_date__lt=(now - datetime.timedelta(minutes=5))).delete()
