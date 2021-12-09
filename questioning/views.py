import json
from django.utils.translation import gettext_lazy as _
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .services import get_result, generate_result, delete_result, get_questions, save_questioning_results, send_result


@method_decorator(csrf_exempt, name='dispatch')
class ResultViewSet(View):
    def get(self, request, link=''):
        if link:
            return render(request, 'questioning_results.html', get_result(link=link))
        else:
            if not request.user.is_authenticated:
                return render(request, 'questioning_results.html', {'title': _("Ви не авторизовані"), })
            return render(request, 'questioning_results.html', get_result(user=request.user))

    def post(self, request):
        questioning_type, results = json.loads(request.read())
        user = request.user
        if user.is_authenticated:
            save_questioning_results(user.id, results, questioning_type)
            send_result(user.email, questioning_type, results)
        return render(request, 'questioning_results.html', generate_result(results, questioning_type))

    def delete(self, request, id):
        if delete_result(id, request.user):
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)


def questioning_view(request):
    return render(request, "questioning.html")


@method_decorator(csrf_exempt, name='dispatch')
class QuestioningViewSet(View):
    def get(self, request, questions_type):
        if questions := get_questions(questions_type):
            return JsonResponse(questions, safe=False)
        else:
            return HttpResponse(status=404)

    def post(self, request, ):
        return HttpResponse(
            loader.get_template('questioning_ajax.html').render(json.loads(request.read()), request))
