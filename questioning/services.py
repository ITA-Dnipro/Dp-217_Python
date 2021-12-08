import json
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from django.template import loader
from questioning.models import TestResult, KlimovCategory, ConnectionKlimovCatStudyField, InterestCategory, \
    ConnectionInterestCatSpec, QuestionsBase
from users.models import CustomUser
from enrollment_assistant.services import produce_message

KLIMOV_QUESTION_TYPE = 1
ALTERNATIVE_KLIMOV_QUESTION_TYPE = 2
HOLAND_QUESTION_TYPE = 3
KLIMOVS_AVERAGE_RESULT = 4
HOLAND_AVERAGE_RESULT = 0
KLIMOVS_DIVIDER = 3
HOLAND_DIVIDER = 4
TITLE = _("Ваші результати")
TITLE_NO_RESULTS = _('Ви не пройшли опитування')
TITLE_NOT_FOUND = _('Результат опитування не знайдено')
KLIMOV_QUESTION_BUTTON_STYLES = ['btn btn-primary',
                                 'btn btn-info']
ALTERNATIVE_KLIMOV_QUESTION_BUTTON_STYLES = ['btn btn-primary',
                                             'btn btn-secondary',
                                             'btn btn-danger']
HOLAND_QUESTION_BUTTON_STYLES = ['btn btn-primary',
                                 'btn btn-info',
                                 'btn btn-secondary',
                                 'btn btn-warning',
                                 'btn btn-danger']
SEARCH_LINK = [_("Посилання на пошук:"), '']
KLIMOVS_SEVERITY = [_("схильність не виражена"),
                    _("середньо виражена схильність"),
                    _("вкрай виражену схильність")]
HOLAND_SEVERITY = [_("інтерес виражений слабо"),
                   _("виражений інтерес"),
                   _("яскраво виражений інтерес")]
KLIMOVS_PART_DESC = _("Професії типу «Людина - ")
HOLAND_PART_DESC = "«"
KLIMOVS_MAX_RESULT = 8
HOLAND_MAX_RESULT = 12
KLIMOVS_SHORT_NAME = _('Людина')
QUESTION_TYPES = [_("Тест на визначення профорієнтації"),
                  _("Тест на визначення профорієнтації"),
                  _("Тест на визначення типу майбутньої професії")]
FROM = _('з')
MARKS = _('балів')
TOPIC_SEND_MAIL = 'send_mail'
KLIMOV_DATABASE = 'KlimovCategory'
HOLAND_DATABASE = 'InterestCategory'
QUESTIONS_DATABASE = 'QuestionsBase'
KLIMOVS_STUDY_FIELDS_DATABASE = 'ConnectionKlimovCatStudyField'
HOLAND_STUDY_FIELDS_DATABASE = 'ConnectionInterestCatSpec'
TEST_RESULT_DATABASE = 'TestResult'
DATABASES = {
    KLIMOV_DATABASE: KlimovCategory,
    HOLAND_DATABASE: InterestCategory,
    QUESTIONS_DATABASE: QuestionsBase,
    KLIMOVS_STUDY_FIELDS_DATABASE: ConnectionKlimovCatStudyField,
    HOLAND_STUDY_FIELDS_DATABASE: ConnectionInterestCatSpec,
    TEST_RESULT_DATABASE: TestResult,
}


def get_cached_database(params):
    try:
        if not cache.get(params):
            cache.set(params, DATABASES[params].objects.all())
        return cache.get(params)
    finally:
        return DATABASES[params].objects.all()


def save_questioning_results(user_id, results, test_type):
    user_id = CustomUser.objects.get(id=user_id)
    TestResult.objects.create(results=results, user_id=user_id, type=test_type)
    get_cached_database(TEST_RESULT_DATABASE)


def get_fields_links(study_fields, item, question_type):
    fields = [SEARCH_LINK]
    for study_field in study_fields.filter(category_id=item):
        if question_type != HOLAND_QUESTION_TYPE:
            name = study_field.field_id.name
            link = name.replace(' ', '_')
        else:
            field = study_field.spec_id.study_field
            name = study_field.spec_id.name
            link = f"_{field}__{name.replace(' ', '_')}"
        fields.append([name, link])
    return fields


def get_average_result(question_type):
    return KLIMOVS_AVERAGE_RESULT if question_type != HOLAND_QUESTION_TYPE else HOLAND_AVERAGE_RESULT


def get_description_info(question_type):
    if question_type != HOLAND_QUESTION_TYPE:
        categories_desc = get_cached_database(KLIMOV_DATABASE)
        study_fields = get_cached_database(KLIMOVS_STUDY_FIELDS_DATABASE).select_related('field_id')
    else:
        categories_desc = get_cached_database(HOLAND_DATABASE)
        study_fields = get_cached_database(HOLAND_STUDY_FIELDS_DATABASE).select_related('spec_id')
    return categories_desc, study_fields


def generate_result(results, question_type=KLIMOV_QUESTION_TYPE):
    categories = []
    categories_desc, study_fields = get_description_info(question_type)
    top_categories = get_top_categories(
        results, get_average_result(question_type)).items()
    for item, result in top_categories:
        fields = get_fields_links(study_fields, item, question_type)
        desc = categories_desc.filter(id=item).first()
        categories.append({'name': get_category_name(question_type, result, desc.name),
                           'desc': desc.desc,
                           'prof': [desc.professions],
                           'study_fields': fields,
                           'id': f"cat_{len(categories)}"})
    resulted_text = {'title': TITLE + ":",
                     'data': [{'categories': categories}]}
    return resulted_text


def get_category_name(question_type, result, name):
    if question_type != HOLAND_QUESTION_TYPE:
        severity = KLIMOVS_SEVERITY
        divider = KLIMOVS_DIVIDER
        part_desc = KLIMOVS_PART_DESC
        max_res = KLIMOVS_MAX_RESULT
    else:
        severity = HOLAND_SEVERITY
        divider = HOLAND_DIVIDER
        part_desc = HOLAND_PART_DESC
        max_res = HOLAND_MAX_RESULT
    severity = severity[result //
                        divider] if result < max_res else severity[-1]
    return f"{part_desc}{name}» - {severity} ({result} {FROM} {max_res} {MARKS})."


def get_top_categories(resulted_categories, average_result=KLIMOVS_AVERAGE_RESULT):
    category = {k: v for k, v in sorted(
        resulted_categories.items(), key=lambda item: item[1], reverse=True)}
    category_dict = {}
    keys = [key for key in category.keys()]

    while keys and category[str(keys[0])] > average_result or len(category_dict) < 3:
        category_dict[keys[0]] = category[keys[0]]
        keys.pop(0)
    return category_dict


def gen_results(answers):
    context = []
    categories_desc = get_cached_database(KLIMOV_DATABASE).values()
    interests_desc = get_cached_database(HOLAND_DATABASE).values()
    study_fields = get_cached_database(KLIMOVS_STUDY_FIELDS_DATABASE).select_related('field_id')
    specialities = get_cached_database(HOLAND_STUDY_FIELDS_DATABASE).select_related('spec_id')
    for answer in answers:
        result, date, url, result_id, question_type = eval(answer['results']), answer['created_date'], answer['url'], \
            answer['id'], answer['type']
        average_result = get_average_result(question_type)
        top_categories = get_top_categories(result, average_result).items()
        categories = []
        for item, _ in top_categories:
            if question_type != HOLAND_QUESTION_TYPE:
                fields = study_fields
                desc = categories_desc.filter(id=item).first()
                name = f"{KLIMOVS_SHORT_NAME} - {desc['name']}"
            else:
                fields = specialities
                desc = interests_desc.filter(id=item).first()
                name = desc['name']
            fields_links = get_fields_links(fields, item, question_type)
            categories.append({'name': name,
                               'prof': desc['professions'].replace('.', '').split(','),
                               'study_fields': fields_links,
                               'id': f"cat_{item}_{len(context)}"})
        context.append({'date': date.strftime("%d/%m/%Y"),
                        'categories': categories,
                        'id': result_id,
                        'url': url,
                        'type': get_question_type(question_type),
                        'short': 1})
    context.reverse()
    return context


def get_result(user='', link=''):
    if link:
        query = get_cached_database(TEST_RESULT_DATABASE).filter(url=link)
        if query:
            results = eval(query.first().results)
            questioning_type = query.first().type
            return generate_result(results, questioning_type)
        else:
            return {'title': TITLE_NOT_FOUND, }
    else:
        items = list(CustomUser.objects.get(
            id=user.id).testresult_set.all().values())
        if len(items) == 0:
            return {'title': TITLE_NO_RESULTS, }
        return {'title': TITLE, 'data': gen_results(items)}


def get_question_type(question_type_index):
    return QUESTION_TYPES[question_type_index - 1]


def get_prof_categories(question_type):
    if question_type != HOLAND_QUESTION_TYPE:
        return {category.id: category.generate_element for category in list(get_cached_database(KLIMOV_DATABASE))}
    else:
        return {category.id: category.generate_element for category in list(get_cached_database(HOLAND_DATABASE))}


def _gen_result(result):
    decoded_result = {
        'categories': [],
        'date': result.created_date,
        'id': result.id,
        'url': result.url
    }
    answers_list = eval(result.results)
    for index, data in get_prof_categories(result.type).items():
        decoded_result['categories'].append(
            {
                'info': data,
                'points': answers_list[str(index)],
                'max_points': KLIMOVS_MAX_RESULT if result.type != HOLAND_QUESTION_TYPE else HOLAND_MAX_RESULT,
            }
        )
    return decoded_result


def get_generated_user_results(user):
    return [_gen_result(result) for result in user.testresult_set.all()]


def get_top_n_results(results, n=3):
    top_n_results = []
    for result in results:
        top_n_results.append(result)
        categories = top_n_results[-1]['categories']
        categories.sort(key=lambda x: x['points'], reverse=True)
        top_n_results[-1]['categories'] = categories[:n]
    return top_n_results


def get_button_styles(questions_type):
    if questions_type == KLIMOV_QUESTION_TYPE:
        return KLIMOV_QUESTION_BUTTON_STYLES
    elif questions_type == ALTERNATIVE_KLIMOV_QUESTION_TYPE:
        return ALTERNATIVE_KLIMOV_QUESTION_BUTTON_STYLES
    else:
        return HOLAND_QUESTION_BUTTON_STYLES


def send_result(user_email, questioning_type, results):
    result = generate_result(results, questioning_type)['data'][0]
    message = loader.render_to_string('result_card.html', {'result': result})
    partition = {'items': [{'mail': user_email,
                 'subject': get_question_type(questioning_type),
                            'text': message}]}
    produce_message(TOPIC_SEND_MAIL, partition)


def delete_result(result_id, user):
    result = get_cached_database(TEST_RESULT_DATABASE).filter(id=result_id).first()
    if result is None or user != result.user_id:
        return False
    result.delete()
    get_cached_database(TEST_RESULT_DATABASE)
    return True


def get_questions(questions_type):
    query = get_cached_database(QUESTIONS_DATABASE).filter(type=questions_type)
    if query:
        question_base = [item.generate_element for item in list(query)]
    else:
        return False
    buttons = get_button_styles(questions_type)
    return json.dumps(
        {'questions': question_base,
         'results': {i: 0 for i in range(1, 20 if questions_type == HOLAND_QUESTION_TYPE else 6)},
         'type': questions_type, 'buttons': buttons})
