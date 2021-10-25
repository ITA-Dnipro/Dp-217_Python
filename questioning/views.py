import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from questioning.models import TestResult, UserTestResult, QuestionsBase
from .services import save_questions_results, create_answer, get_all_answers


def questioning_view(request):
    return render(request, "questioning.html")


def remove_result(request, url):
    return delete_result(request, TestResult.objects.get(url=url))


@csrf_exempt
def questioning_ajax(request):
    tmp = json.loads(request.read())
    t = loader.get_template('questioning_ajax.html')
    return HttpResponse(t.render(tmp, request))


@csrf_exempt
def questioning_results(request, link=''):
    if request.is_ajax():
        results = json.loads(request.read())
        save_questions_results(request, results)
        resulted_text = create_answer(results)
        return render(request, 'questioning_results.html', resulted_text)
    if link == '':
        title = get_all_answers(request)
    else:
        query = TestResult.objects.filter(url=link)
        if query:
            results = query.first().results
            results = [int(i) for i in results[1:-1].replace(' ', '').split(',')]
            resulted_text = create_answer(results)
            return render(request, 'questioning_results_current.html', resulted_text)
        else:
            title = {'title': 'Результат опитування не знайдено', }
    return render(request, 'questioning_results_full.html', title)


@csrf_exempt
def delete_result(request, id):
    result = get_object_or_404(UserTestResult, result_id=id)

    if request.user != result.user_id:
        return HttpResponse(status=403)

    result.delete()
    return HttpResponse(status=200)


def get_questions(request, questions_type):
    qs = list(QuestionsBase.objects.filter(type=questions_type).values())
    qs = [{'questions': qs, 'results': [], }]
    return JsonResponse(json.dumps(qs), safe=False)
