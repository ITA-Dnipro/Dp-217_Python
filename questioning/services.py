import json
from questioning.models import TestResult, KlimovCategory
from users.models import CustomUser


def save_questions_results(user_id, results):
    user_id = CustomUser.objects.get(id=user_id)
    TestResult.objects.create(results=results, user_id=user_id)


def gen_result(results):
    categorised_results = {i: results.count(i) for i in set(results)}
    top_categories = get_top_categories(categorised_results)
    categories_desc = KlimovCategory.objects.all().values()
    desc = []
    professions = []
    result_desc = []
    part_res_desc = "Професії типу «Людина - "
    expression = ["схильність не виражена", "середньо виражена схильність", "вкрай виражену схильність"]
    title = "Ваші результати:"
    professions_options = "Ви можете почати освоювати одну з відповідних вам професій:"
    new_line = '\n'
    for item in top_categories:
        category = categories_desc[item]['name']
        desc.append(categories_desc[item]['desc'])
        professions.append(categories_desc[item]['professions'])
        result = categorised_results[item]
        expression_id = result // 3
        result_desc.append(
            f"{part_res_desc}{category}» - {expression[expression_id]} ({result} з 8 балів).")

    resulted_text = {
        'title': title,
        'first_desc': desc[0], 'second_desc': desc[1], 'third_desc': desc[2],
        'first_professions': f"{professions_options}{new_line}{professions[0]}",
        'second_professions': f"{professions_options}{new_line}{professions[1]}",
        'third_professions': f"{professions_options}{new_line}{professions[2]}",
        'first_result': result_desc[0],
        'second_result': result_desc[1],
        'third_result': result_desc[2],
    }
    return resulted_text


def gen_results(answers):
    items = []
    categories_desc = KlimovCategory.objects.all().values()
    for answer in answers:
        result, date, url = eval(answer['results']), answer['created_date'], answer['url']
        top_categories = get_top_categories({i: result.count(i) for i in set(result)})
        items.append([date.strftime("%d/%m/%Y"),
                      categories_desc[top_categories[0]]['name'],
                      categories_desc[top_categories[1]]['name'],
                      categories_desc[top_categories[2]]['name'],
                      categories_desc[top_categories[0]]['professions'],
                      categories_desc[top_categories[1]]['professions'],
                      categories_desc[top_categories[2]]['professions'],
                      url])
    items.sort(reverse=True)
    return items


def get_results(user_id):
    user = CustomUser.objects.get(id=user_id)
    items = [user_result for user_result in user.testresult_set.all().values('created_date', 'results', 'url')]
    if len(items) == 0:
        return {'title': 'Ви не пройшли опитування', }
    items = gen_results(items)
    context = [{'date': 'Дата', 'categories': 'Категорії результату', 'professions': 'Рекомендовані професії', }]
    for item in items:
        context.append({'date': item[0], 'categories': item[1:4], 'professions': item[4:-1],
                        'url': item[-1], })
    return {'title': 'Ваші результати', 'data': json.dumps(context)}


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

    answers_list = json.loads(result.results)
    for index, data in gen_prof_categories().items():
        decoded_result['categories'].append(
            {
                'info': data,
                'points': answers_list.count(index),
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
