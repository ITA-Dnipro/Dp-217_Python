import json
from questioning.models import TestResult, KlimovCategory, ConnectionKlimovCatStudyField, InterestCategory, \
    ConnectionInterestCatSpec, QuestionsBase
from users.models import CustomUser


def save_questions_results(user_id, results, test_type):
    user_id = CustomUser.objects.get(id=user_id)
    TestResult.objects.create(results=results, user_id=user_id, type=test_type)


def get_parameters(question_type):
    if question_type != 3:
        average_result = 4
        categories_desc = KlimovCategory.objects.all().values()
        study_fields = ConnectionKlimovCatStudyField.objects.select_related('field_id').all()
        severity = ["схильність не виражена", "середньо виражена схильність", "вкрай виражену схильність"]
        divider = 3
        part_desc = "Професії типу «Людина - "
        max_res = 8
    else:
        average_result = 0
        categories_desc = InterestCategory.objects.all().values()
        study_fields = ConnectionInterestCatSpec.objects.select_related('spec_id').all()
        severity = ["інтерес виражений слабо", "виражений інтерес", "яскраво виражений інтерес"]
        divider = 4
        part_desc = "«"
        max_res = 12
    return average_result, categories_desc, study_fields, divider, severity, part_desc, max_res


def get_fields_links(study_fields, item, question_type):
    fields = [["Посилання на пошук:", '']]
    if question_type != 3:
        for study_field in study_fields.filter(category_id=item):
            name = study_field.field_id.name
            fields.append([name, name.replace(' ', '_')])
        return fields
    for study_field in study_fields.filter(category_id=item):
        field = study_field.spec_id.study_field
        name = study_field.spec_id.name
        fields.append([name, f"_{field}__{name.replace(' ', '_')}"])
    return fields


def gen_result(results, question_type=1):
    average_result, categories_desc, study_fields, divider, severity, part_desc, max_res = get_parameters(question_type)
    top_categories = get_top_categories(results, average_result)
    title = "Ваші результати:"
    categories = []
    for item, result in top_categories.items():
        fields = get_fields_links(study_fields, item, question_type)
        desc = categories_desc.filter(id=item).first()
        name = f"{part_desc}{desc['name']}»"
        categories.append({'name': f"{name} - {severity[result // divider]} ({result} з {max_res} балів).",
                           'desc': desc['desc'],
                           'prof': [desc['professions']],
                           'study_fields': fields, 'id': f"cat_{len(categories)}"})
    resulted_text = {'title': title, 'data': [{'categories': categories}]}
    return resulted_text


def get_top_categories(resulted_categories, average_result=4):
    cat = {k: v for k, v in sorted(resulted_categories.items(), key=lambda item: item[1], reverse=True)}
    cat_dict = {}
    for key, value in cat.items():
        if value > average_result or len(cat_dict) < 3:
            cat_dict[key] = value
        else:
            break
    return cat_dict


def gen_results(answers):
    context = []
    categories_desc = KlimovCategory.objects.all().values()
    interests_desc = InterestCategory.objects.all().values()
    study_fields = ConnectionKlimovCatStudyField.objects.select_related('field_id').all()
    specialities = ConnectionInterestCatSpec.objects.select_related('spec_id').all()
    for answer in answers:
        result, date, url, result_id, question_type = eval(answer['results']), answer['created_date'], answer['url'], \
                                                      answer['id'], answer['type']
        categories = []
        if question_type != 3:
            for item, _ in get_top_categories(result).items():
                fields = get_fields_links(study_fields, item, question_type)
                desc = categories_desc.filter(id=item).first()
                categories.append({'name': f"Людина - {desc['name']}",
                                   'prof': desc['professions'].replace('.', '').split(','),
                                   'study_fields': fields, 'id': f"cat_{item}_{len(context)}"})
        else:
            for item, _ in get_top_categories(result, 0).items():
                fields = get_fields_links(specialities, item, question_type)
                desc = interests_desc.filter(id=item).first()
                categories.append({'name': desc['name'],
                                   'prof': desc['professions'].replace('.', '').split(','),
                                   'study_fields': fields, 'id': f"cat_{item}_{len(context)}"})
        context.append({'date': date.strftime("%d/%m/%Y"), 'categories': categories, 'id': result_id, 'url': url,
                        'type': get_question_type(question_type), 'short': 1})
    context.reverse()
    return context


def get_results(user):
    if not user.is_authenticated:
        return {'title': "Ви не авторизовані", }
    items = list(CustomUser.objects.get(id=user.id).testresult_set.all().values())
    if len(items) == 0:
        return {'title': 'Ви не пройшли опитування', }
    return {'title': 'Ваші результати', 'data': gen_results(items)}


def get_question_type(question_type_index):
    desc_question_types = ["Тест на визначення профорієнтації", "Тест на визначення профорієнтації",
                           "Тест на визначення типу майбутньої професії"]
    return desc_question_types[question_type_index - 1]


def gen_prof_categories():
    return {index: category.generate_element for index, category in enumerate(KlimovCategory.objects.all())}


def decode_result(result):
    decoded_result = {
        'categories': [],
        'date': result.created_date,
        'id': result.id,
        'url': result.url
    }
    answers_list = eval(result.results)
    if result.type != 3:
        for index, data in gen_prof_categories().items():
            decoded_result['categories'].append(
                {
                    'info': data,
                    'points': answers_list[index + 1],
                }
            )
    return decoded_result


def get_decoded_user_results(user):
    return [decode_result(result) for result in user.testresult_set.all()]


def make_top_n_results(results, n=3):
    for result in results:
        categories = result['categories']
        categories.sort(key=lambda x: x['points'], reverse=True)
        result['categories'] = categories[:n]
    return


def get_button_styles(questions_type):
    if questions_type == 1:
        return ['btn btn-primary', 'btn btn-info']
    elif questions_type == 2:
        return ['btn btn-primary', 'btn btn-secondary', 'btn btn-danger']
    else:
        return ['btn btn-primary', 'btn btn-info', 'btn btn-secondary', 'btn btn-warning', 'btn btn-danger']


def get_result(link):
    query = TestResult.objects.filter(url=link)
    if query:
        return gen_result(eval(query.first().results), query.first().type)
    else:
        return {'title': 'Результат опитування не знайдено', }


def generate_result(result, user):
    result = json.loads(result)
    if user.is_authenticated:
        save_questions_results(user.id, result[1], result[0])
    return gen_result(result[1], result[0])


def delete_result(result_id, user):
    result = TestResult.objects.filter(id=result_id).first()
    if (result is None) or (user != result.user_id):
        return False
    result.delete()
    return True


def get_questions(questions_type):
    question_base = [item.generate_element for item in list(QuestionsBase.objects.filter(type=questions_type))]
    buttons = get_button_styles(questions_type)
    return json.dumps(
        {'questions': question_base, 'results': {i: 0 for i in range(1, 20 if questions_type == 3 else 6)},
         'type': questions_type, 'buttons': buttons})
