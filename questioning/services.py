from questioning.models import TestResult, KlimovCategory, ConnectionKlimovCatStudyField, InterestCategory, \
    ConnectionInterestCatSpec
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


def gen_result(results, question_type):
    average_result, categories_desc, study_fields, divider, severity, part_desc, max_res = get_parameters(question_type)
    top_categories = get_top_categories(results, average_result)
    title = "Ваші результати:"
    categories = []
    for item in top_categories:
        numerator = item - 1 if question_type != 3 else item
        fields = get_fields_links(study_fields, item, question_type)
        result = results[item]
        severity_id = result // divider
        name = f"{part_desc}{categories_desc[numerator]['name']}»"
        categories.append(
            {'name': f"{name} - {severity[severity_id]} ({result} з {max_res} балів).",
             'desc': categories_desc[numerator]['desc'],
             'prof': [categories_desc[numerator]['professions']],
             'study_fields': fields, 'id': f"cat_{len(categories)}"})
    resulted_text = {'title': title, 'data': [{'categories': categories}]}
    return resulted_text


def get_top_categories(resulted_categories, average_result=4):
    cat = resulted_categories.copy()
    max_key = []
    max_key_current = max(cat, key=cat.get)
    while len(max_key) < 3 or cat.get(max_key_current) > average_result:
        max_key.append(max_key_current)
        cat[max_key[-1]] = 0
        max_key_current = max(cat, key=cat.get)
    return max_key


def gen_results(answers):
    context = []
    categories_desc = KlimovCategory.objects.all().values()
    interests_desc = InterestCategory.objects.all().values()
    study_fields = ConnectionKlimovCatStudyField.objects.select_related('field_id').all()
    specialities = ConnectionInterestCatSpec.objects.select_related('spec_id').all()
    for answer in answers:
        result, date, url, result_id, question_type = eval(answer['results']), answer['created_date'], answer['url'], \
                                                      answer['id'], answer['type']
        if question_type != 3:
            categories = []
            for item in get_top_categories(result):
                item = item - 1
                fields = get_fields_links(study_fields, item, question_type)
                categories.append({'name': f"Людина - {categories_desc[item]['name']}",
                                   'prof': categories_desc[item]['professions'].replace('.', '').split(','),
                                   'study_fields': fields, 'id': f"cat_{item}_{len(context)}"})
        else:
            categories = []
            for item in get_top_categories(result, 0):
                fields = get_fields_links(specialities, item, question_type)
                categories.append({'name': interests_desc[item]['name'],
                                   'prof': interests_desc[item]['professions'].replace('.', '').split(','),
                                   'study_fields': fields, 'id': f"cat_{item}_{len(context)}"})
        context.append({'date': date.strftime("%d/%m/%Y"), 'categories': categories, 'id': result_id, 'url': url,
                        'type': get_question_type_name(question_type), 'short': 1})
    context.reverse()
    return context


def get_results(user_id):
    user = CustomUser.objects.get(id=user_id)
    items = [user_result for user_result in
             user.testresult_set.all().values('created_date', 'results', 'url', 'id', 'type')]
    if len(items) == 0:
        return {'title': 'Ви не пройшли опитування', }
    return {'title': 'Ваші результати', 'data': gen_results(items)}


def get_question_type_name(question_type_index):
    desc_question_types = ["Тест на визначення профорієнтації", "Тест на визначення типу майбутньої професії",
                           "Тест на визначення типу майбутньої професії"]
    return desc_question_types[question_type_index - 1]


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
                'points': answers_list[index + 1],
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
    if question_type == 2:
        answer = {}
        for item in result:
            if item != 0:
                item = str(item)
                if answer.get(int(item[0])):
                    answer[int(item[0])] += int(item[1]) if item[2] == '0' else -int(item[1])
                else:
                    answer[int(item[0])] = int(item[1]) if item[2] == '0' else -int(item[1])
        return answer
    if question_type == 3:
        answer = {}
        for item in result:
            if item != 0:
                index_val = item % 10
                index = item // 10
                val = 2 if index_val == 2 or index_val == 3 else 1
                val = val if index_val == 0 or index_val == 1 else -val
                if answer.get(index):
                    answer[index] += val
                else:
                    answer[index] = val
        return answer
