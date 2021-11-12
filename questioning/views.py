import json
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .services import get_result, get_results, generate_result, delete_result, get_questions


@method_decorator(csrf_exempt, name='dispatch')
class ResultViewSet(View):
    def get(self, request, link=''):
        if link:
            return render(request, 'questioning_results.html', get_result(link))
        else:
            return render(request, 'questioning_results.html', get_results(request.user))

    def post(self, request):
        return render(request, 'questioning_results.html', generate_result(request.read(), request.user))

    def delete(self, request, id):
        if delete_result(id, request.user):
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=403)


def questioning_view(request):
    return render(request, "questioning.html")


@method_decorator(csrf_exempt, name='dispatch')
class QuestioningViewSet(View):
    def get(self, request, questions_type):
        return JsonResponse(get_questions(questions_type), safe=False)

    def post(self, request, ):
        return HttpResponse(
            loader.get_template('questioning_ajax.html').render(json.loads(request.read()), request))
