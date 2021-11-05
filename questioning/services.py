import json
from questioning.models import TestResult, KlimovCategory, ConnectionKlimovCatStudyField
from users.models import CustomUser


def save_questions_results(user_id, results, test_type):
    user_id = CustomUser.objects.get(id=user_id)
    TestResult.objects.create(results=results, user_id=user_id, type=test_type)


def gen_result(results):
    top_categories = get_top_categories(results)
    categories_desc = KlimovCategory.objects.all().values()
    study_fields = ConnectionKlimovCatStudyField.objects.select_related('field_id').all()
    desc = []
    professions = []
    result_desc = []
    fields = []
    part_res_desc = "Професії типу «Людина - "
    expression = ["схильність не виражена", "середньо виражена схильність", "вкрай виражену схильність"]
    title = "Ваші результати:"
    professions_options = "Ви можете почати освоювати одну з відповідних вам професій:"
    for item in top_categories:
        category = categories_desc[item - 1]['name']
        fields.append([["Посилання на пошук:", '']])
        for study_field in study_fields.filter(category_id=item):
            fields[-1].append([study_field.field_id.name, study_field.field_id.name.replace(' ', '_')])
        desc.append(categories_desc[item - 1]['desc'])
        professions.append([professions_options, categories_desc[item - 1]['professions']])
        result = results[item]
        expression_id = result // 3
        result_desc.append(
            f"{part_res_desc}{category}» - {expression[expression_id]} ({result} з 8 балів).")

    resulted_text = {
        'title': title,
        'data': [{'categories': [
            {'name': result_desc[index], 'desc': desc[index], 'prof': professions[index],
             'study_fields': fields[index], 'id': f"cat_{index}"} for index in range(3)], }]
    }
    return resulted_text


def gen_results(answers):
    items = []
    categories_desc = KlimovCategory.objects.all().values()
    study_fields = ConnectionKlimovCatStudyField.objects.select_related('field_id').all()
    for answer in answers:
        result, date, url, result_id = eval(answer['results']), answer['created_date'], answer['url'], answer['id']
        top_categories = get_top_categories(result)
        fields = []
        for item in top_categories:
            fields.append([])
            for study_field in study_fields.filter(category_id=item):
                fields[-1].append([study_field.field_id.name, study_field.field_id.name.replace(' ', '_')])
        items.append([date.strftime("%d/%m/%Y"),
                      categories_desc[top_categories[0] - 1]['name'],
                      categories_desc[top_categories[1] - 1]['name'],
                      categories_desc[top_categories[2] - 1]['name'],
                      categories_desc[top_categories[0] - 1]['professions'],
                      categories_desc[top_categories[1] - 1]['professions'],
                      categories_desc[top_categories[2] - 1]['professions'],
                      fields[0], fields[1], fields[2], result_id, url])
        items.sort(reverse=True)
    return items


def get_results(user_id):
    user = CustomUser.objects.get(id=user_id)
    items = [user_result for user_result in user.testresult_set.all().values('created_date', 'results', 'url', 'id')]
    if len(items) == 0:
        return {'title': 'Ви не пройшли опитування', }
    items = gen_results(items)
    context = []
    for item in items:
        context.append({'date': item[0], 'categories': [
            {'name': f"Людина - {item[index]}", 'prof': item[index + 3].replace('.', '').split(','),
             'study_fields': item[index + 6], 'id': f"cat_{index}_{len(context)}"} for index in range(1, 4)],
                        'id': item[-2],
                        'url': item[-1], })
    return {'title': 'Ваші результати', 'data': context}


def get_top_categories(resulted_categories):
    resulted_categories_current = resulted_categories.copy()
    max_key = []
    while len(max_key) < 3:
        max_key.append(max(resulted_categories_current, key=resulted_categories_current.get))
        resulted_categories_current[max_key[-1]] = 0
    return max_key


def gen_prof_categories():
    prof_categories = {}
    klimov_category_list = list(KlimovCategory.objects.all().values('name', 'professions', 'desc'))
    for data in klimov_category_list:
        index = klimov_category_list.index(data)
        categories = {'name': f"Людина - {data['name']}", 'examples': data.pop('professions'),
                      'description': data.pop('desc')}
        prof_categories[index] = categories
    return prof_categories


def decode_result(result):
    decoded_result = {
        'categories': [],
        'date': result.created_date,
        'id': result.id,
        'url': result.url
    }
    answers_list = eval(result.results)
    for index, data in gen_prof_categories().items():
        decoded_result['categories'].append(
            {
                'info': data,
                'points': answers_list[index+1],
            }
        )
    return decoded_result


def get_decoded_user_results(user):
    raw_results = [user_result for user_result in user.testresult_set.all()]
    decoded_results = [decode_result(result) for result in raw_results]
    return decoded_results


def make_top_n_results(results, n=3):
    for result in results:
        categories = result['categories']
        categories.sort(key=lambda x: x['points'], reverse=True)
        del categories[-(len(categories) - n):]
    return


def sort_result(result, question_type):
    if question_type == 1:
        return {i: result.count(i) for i in set(result)}
