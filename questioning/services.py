import json
from django.db.models import Prefetch
from questioning.models import TestResult, UserTestResult, KlimovCategory
from users.models import CustomUser

PROF_CATEGORIES = {
    0: {
        'name': 'Людина - природа',
        'examples': "Ландшафтний дизайнер, фотограф, Кінолог, Ветеринар, Агроном, Еколог, Технолог харчової "
                    "промисловості",
        'description': "Сфера діяльності даного типу спрямована на навколишнє нас природу. Це такі професії як "
                       "ветеринар, еколог, агроном, геолог, мікробіолог. Професійно важливими якостями даних професій "
                       "є: інтуїція, емпатія, вміння піклуватися про кого-небудь крім себе. Такі люди зазвичай "
                       "трепетно ставляться до представників живої природи. Для успішної діяльності в професіях цього "
                       "типу недостатньо просто бути любителем відпочинку на природі, важливо ще захищати природу, "
                       "прагнути позитивно взаємодіяти з нею."
    },

    1: {
        'name': 'Людина - техніка',
        'examples': "Автомеханік, Інженер, Електрик, Пілот",
        'description': "Професії даного типу спрямовані на експлуатацію різних технічних пристроїв і приладів, їх "
                       "обслуговування та створення. До таких професій належать: металург, водії різного транспорту, "
                       "пілоти, слюсарі, технологи на підприємствах, будівельники, автомеханіки і т.д. Для їх успішної "
                       "діяльності вкрай важливі технічний склад розуму, уважність, схильність до дій, а не роздумів."
    },

    2: {
        'name': 'Людина - людина',
        'examples': "Психологія, SMM-менеджер, Інтернет-маркетолог, Project-менеджер, Маркетинг, Управління.",
        'description': "До цього типу належать професії, основний напрямок яких пов'язано зі спілкуванням між людьми і "
                       "їх взаємний вплив. Такі як, доктор, викладач, менеджер, учитель, психолог, продавець, тренер. "
                       "Важливим якістю в даних професіях є не тільки бажання, але й вміння активної взаємодії з "
                       "людьми і продуктивного спілкування. Важливо специфікою при підготовці є добре знання "
                       "професійної сфери і розвинені комунікативні навички."
    },

    3: {
        'name': 'Людина - знакова система',
        'examples': "Data Science, програміст Python, розробка мобільних додатків, інтернет-маркетолог.",
        'description': "Основним напрямком діяльності даного типу професій є робота з цифрами, формулами, "
                       "розрахунками, текстами, базами даних. Це такі професії як програміст, економіст, редактор, "
                       "аналітик, перекладач, датасайнтіст, бухгалтер. Професійно важливі якості даного типу професій: "
                       "точність і аналітичний склад розуму, уважність, логічне мислення. Для успішної діяльності "
                       "важливо мати інтерес до різних формулам, таблицям, картам, схемами, баз даних."
    },

    4: {
        'name': 'Людина - художній образ',
        'examples': "Дизайнер, Кліпмейкер, Кіноактор, ТВ - Байєр",
        'description': "Професії даного типу підходять людям з розвиненим образним мисленням і творчою жилкою. Фахівці "
                       "працюють в напрямку «людина - художній образ», обдаровані талантом або мають покликання до "
                       "цього з малих років. Їх діяльність пов'язана з проектуванням, створенням, моделюванням, "
                       "виготовленням різних творів мистецтва."
    },
}


def save_questions_results(request, results):
    if request.user.is_authenticated:
        test_result = TestResult.objects.create(results=results)
        user_id = CustomUser.objects.get(id=request.user.id, )
        UserTestResult.objects.create(user_id=user_id, result_id=test_result)


def create_answer(results):
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
        'first_desc': desc[0],
        'second_desc': desc[1],
        'third_desc': desc[2],
        'first_professions': f"{professions_options}{new_line}{professions[0]}",
        'second_professions': f"{professions_options}{new_line}{professions[1]}",
        'third_professions': f"{professions_options}{new_line}{professions[2]}",
        'first_result': result_desc[0],
        'second_result': result_desc[1],
        'third_result': result_desc[2],
    }
    return resulted_text


def gen_result(results, dates, urls):
    items = []
    categories_desc = KlimovCategory.objects.all().values()
    for index in range(len(urls)):
        result, date, url = results[index], dates[index], urls[index]
        result = [int(i) for i in result[1:-1].replace(' ', '').split(',')]
        categorised_results = {i: result.count(i) for i in set(result)}
        top_categories = get_top_categories(categorised_results)
        items.append([date.strftime("%d/%m/%Y"),
                      categories_desc[top_categories[0]]['name'],
                      categories_desc[top_categories[1]]['name'],
                      categories_desc[top_categories[2]]['name'],
                      categories_desc[top_categories[0]]['professions'],
                      categories_desc[top_categories[1]]['professions'],
                      categories_desc[top_categories[2]]['professions'],
                      url])
    return items


def get_all_answers(request):
    results = get_user_results(request)
    if results == "NotAuthorised":
        return {'title': "Ви не авторизовані", }
    elif len(results) == 0:
        return {'title': 'Ви не пройшли опитування', }
    else:
        urls = []
        for item in results:
            urls.append(str(item))
        urls.reverse()
        all_objects = TestResult.objects.all()
        dates = [record.created_date for record in all_objects if record.url in urls]
        items = [record.results for record in all_objects if record.url in urls]
        items = reversed(gen_result(items, dates, urls))
        context = [{'date': 'Дата', 'categories': 'Категорії результату', 'professions': 'Рекомендовані професії', }]
        for item in items:
            context.append({'date': item[0], 'categories': item[1:4], 'professions': item[4:-1],
                            'url': item[-1], })
    title = {'title': 'Ваші результати', 'data': json.dumps(context)}
    return title


def get_user_results(request):
    if request.user.is_authenticated:
        return UserTestResult.objects.filter(user_id=request.user.id).prefetch_related(
            Prefetch('result_id', queryset=TestResult.objects.all()))
    else:
        return "NotAuthorised"


def get_top_categories(resulted_categories):
    resulted_categories_current = resulted_categories.copy()
    max_key = []
    while len(max_key) < 3:
        max_key.append(max(resulted_categories_current, key=resulted_categories_current.get))
        resulted_categories_current[max_key[-1]] = 0
    return max_key


def decode_result(result):
    decoded_result = {
        'categories': [],
        'date': result.created_date,
        'id': result.id
    }

    answers_list = json.loads(result.results)

    for index, data in PROF_CATEGORIES.items():
        decoded_result['categories'].append(
            {
                'info': data,
                'points': answers_list.count(index),
            }
        )

    return decoded_result


def get_decoded_user_results(user):
    raw_results = [user_result.result_id for user_result in user.usertestresult_set.all()]
    decoded_results = [decode_result(result) for result in raw_results]
    return decoded_results


def make_top_n_results(results, n):
    for result in results:
        categories = result['categories']
        categories.sort(key=lambda x: x['points'], reverse=True)
        del categories[-(len(categories) - n):]
    return
