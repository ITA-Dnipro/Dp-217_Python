import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from questioning.models import TestResult, QuestionsBase
from .services import save_questions_results, gen_result, get_results, sort_result


def questioning_view(request):
    return render(request, "questioning.html")


@csrf_exempt
def questioning_ajax(request):
    tmp = json.loads(request.read())
    t = loader.get_template('questioning_ajax.html')
    return HttpResponse(t.render(tmp, request))


@csrf_exempt
def questioning_results(request, link=''):
    if request.is_ajax():
        results = json.loads(request.read())
        sorted_result = sort_result(results[1], results[0])
        if request.user.is_authenticated:
            save_questions_results(request.user.id, sorted_result, results[0])
        resulted_text = gen_result(sorted_result)
    elif link == '':
        resulted_text = {'title': "Ви не авторизовані", }
        if request.user.is_authenticated:
            resulted_text = get_results(request.user.id)
        return render(request, 'questioning_results.html', resulted_text)
    else:
        query = TestResult.objects.filter(url=link)
        if query:
            resulted_text = gen_result(eval(query.first().results), query.first().type)
        else:
            resulted_text = {'title': 'Результат опитування не знайдено', }
    return render(request, 'questioning_results.html', resulted_text)


@csrf_exempt
def delete_result(request, id):
    result = get_object_or_404(TestResult, id=id)

    if request.user != result.user_id:
        return HttpResponse(status=403)

    result.delete()
    return HttpResponse(status=200)


def get_questions(request, questions_type):
    question_base = []
    questions = list(QuestionsBaseNew.objects.filter(type=questions_type).values())
    for item in questions:
        question_base.append({'question': item['question'], 'answers': [{
            'text': text, 'result': result} for text, result in
            zip(item['answer'].split('__'), item['result'].split('__'))]})
    return JsonResponse(
        json.dumps({'questions': question_base, 'results': [], 'type': questions_type, 'size': len(questions)}),
        safe=False)
