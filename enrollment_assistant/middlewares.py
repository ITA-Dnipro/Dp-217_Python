from django.http import HttpResponse
from universearch.services import get_universities
from requests.exceptions import ConnectionError


class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, ConnectionError):
            return HttpResponse("Помилка з'єднання. Спробуйте пізніше", status=500)
        else:
            return HttpResponse('Помилка. Спробуйте пізніше')

