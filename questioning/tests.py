import json
from django.test import TestCase
from django.utils import timezone
from questioning.cron import remove_obsolete_records
from questioning.models import TestResult, KlimovCategory
from questioning.services import save_questions_results, gen_result, gen_results, get_results, get_top_categories, \
    decode_result, get_decoded_user_results, make_top_n_results, gen_prof_categories
from users.models import CustomUser

RESULTS = "[1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0]"


class CronTestCase(TestCase):
    created_date = timezone.now() - timezone.timedelta(days=367)

    def test_cron1(self):
        CustomUser.objects.create(email='admin')
        user_id = CustomUser.objects.all().last()
        TestResult.objects.create(results=RESULTS, created_date=self.created_date, user_id=user_id)
        TestResult.objects.create(results=RESULTS, created_date=self.created_date, user_id=user_id)
        self.assertEqual(len(TestResult.objects.all()), 2)
        remove_obsolete_records()
        self.assertEqual(len(TestResult.objects.all()), 0)

    def test_cron2(self):
        CustomUser.objects.create(email='admin')
        user_id = CustomUser.objects.all().last()
        TestResult.objects.create(results=RESULTS, created_date=self.created_date, user_id=user_id)
        test_id = TestResult.objects.create(results=RESULTS, user_id=user_id).id
        self.assertEqual(len(TestResult.objects.all()), 2)
        remove_obsolete_records()
        self.assertTrue(TestResult.objects.get(id=test_id))

    def test_cron3(self):
        CustomUser.objects.create(email='admin')
        user_id = CustomUser.objects.all().last()
        TestResult.objects.create(results=RESULTS, user_id=user_id)
        TestResult.objects.create(results=RESULTS, user_id=user_id)
        self.assertEqual(len(TestResult.objects.all()), 2)
        remove_obsolete_records()
        self.assertEqual(len(TestResult.objects.all()), 2)


class SaveTestCase(TestCase):
    user_id = 0

    def setUp(self):
        CustomUser.objects.create(email='admin')
        self.user_id = CustomUser.objects.all().last().id

    def test_save1(self):
        self.assertEqual(len(TestResult.objects.all()), 0)
        save_questions_results(user_id=self.user_id, results=RESULTS)
        self.assertEqual(len(TestResult.objects.all()), 1)


class GenResultTestCase(TestCase):
    fixtures = ['klimovcategory.json', ]

    def test_gen_result(self):
        test_answer = {
            'title': "Ваші результати:",
            'first_desc': "Сфера діяльності даного типу спрямована на навколишнє нас природу. Це такі професії як "
                          "ветеринар, еколог, агроном, геолог, мікробіолог. Професійно важливими якостями даних "
                          "професій є: інтуїція, емпатія, вміння піклуватися про кого-небудь крім себе. Такі люди "
                          "зазвичай трепетно ставляться до представників живої природи. Для успішної діяльності в "
                          "професіях цього типу недостатньо просто бути любителем відпочинку на природі, важливо ще "
                          "захищати природу, прагнути позитивно взаємодіяти з нею.",
            'second_desc': "Професії даного типу спрямовані на експлуатацію різних технічних пристроїв і приладів, їх "
                           "обслуговування та створення. До таких професій належать: металург, водії різного "
                           "транспорту, пілоти, слюсарі, технологи на підприємствах, будівельники, автомеханіки і т.д. "
                           "Для їх успішної діяльності вкрай важливі технічний склад розуму, уважність, схильність до "
                           "дій, а не роздумів.",
            'third_desc': "До цього типу належать професії, основний напрямок яких пов'язано зі спілкуванням між людьми"
                          " і їх взаємний вплив. Такі як, доктор, викладач, менеджер, учитель, психолог, продавець, "
                          "тренер. Важливим якістю в даних професіях є не тільки бажання, але й вміння активної "
                          "взаємодії з людьми і продуктивного спілкування. Важливою специфікою при підготовці є добрі "
                          "знання професійної сфери і розвинені комунікативні навички.",
            'first_professions': "Ви можете почати освоювати одну з відповідних вам професій:\n"
                                 "Ландшафтний дизайнер, Фотограф, Кінолог, Ветеринар, Агроном, Еколог, Технолог "
                                 "харчової промисловості.",
            'second_professions': "Ви можете почати освоювати одну з відповідних вам професій:\n"
                                  "Автомеханік, Інженер, Електрик, Пілот.",
            'third_professions': "Ви можете почати освоювати одну з відповідних вам професій:\n"
                                 "Психолог, SMM-менеджер, Інтернет-маркетолог, Project-менеджер, Маркетинг, Управління"
                                 ".",
            'first_result': 'Професії типу «Людина - природа» - середньо виражена схильність (4 з 8 балів).',
            'second_result': 'Професії типу «Людина - техніка» - середньо виражена схильність (4 з 8 балів).',
            'third_result': 'Професії типу «Людина - людина» - середньо виражена схильність (4 з 8 балів).',
        }
        answer = gen_result(eval(RESULTS))
        self.assertEqual(answer, test_answer)


class GenResultsTestCase(TestCase):
    fixtures = ['klimovcategory.json', ]

    def test_gen_results(self):
        url = '72f126da7df6798cd22c5bb5d6aab5d7'
        test_answer = [
            [timezone.now().strftime("%d/%m/%Y"),
             'природа',
             'техніка',
             'людина',
             'Ландшафтний дизайнер, Фотограф, Кінолог, Ветеринар, Агроном, Еколог, '
             'Технолог харчової промисловості.',
             'Автомеханік, Інженер, Електрик, Пілот.',
             'Психолог, SMM-менеджер, Інтернет-маркетолог, Project-менеджер, Маркетинг, '
             'Управління.',
             url]
        ]
        answer = gen_results([RESULTS], [timezone.now()], [url])
        self.assertEqual(answer, test_answer)


class GetResultsTestCase(TestCase):
    fixtures = ['klimovcategory.json', ]

    def test_gen_results1(self):
        test_answer = {'title': 'Ви не пройшли опитування', }
        answer = get_results(0)
        self.assertEqual(answer, test_answer)

    def test_gen_results2(self):
        user_id = CustomUser.objects.create(email='admin')
        url = TestResult.objects.create(results=RESULTS, user_id=user_id).url
        items = gen_results([RESULTS], [timezone.now()], [url])
        context = [{'date': 'Дата', 'categories': 'Категорії результату',
                    'professions': 'Рекомендовані професії', }, ]
        for item in items:
            context.append({'date': item[0], 'categories': item[1:4], 'professions': item[4:-1], 'url': item[-1], })
        test_answer = {'title': 'Ваші результати', 'data': json.dumps(context)}
        answer = get_results(user_id.id)
        self.assertEqual(answer, test_answer)


class GetTopCategoriesTestCase(TestCase):
    def test_gen_results1(self):
        test_answer = [0, 1, 2]
        result = eval(RESULTS)
        answer = get_top_categories({i: result.count(i) for i in set(result)})
        self.assertEqual(answer, test_answer)


def get_answer(result_id, created_date, url):
    answers_list = eval(RESULTS)
    answer = {'categories': [], 'date': created_date, 'id': result_id, 'url': url}
    klimov_category_list = list(KlimovCategory.objects.all().values('name', 'professions', 'desc'))
    for data in klimov_category_list:
        index = klimov_category_list.index(data)
        data['name'] = f"Людина - {data['name']}"
        data['examples'] = data.pop('professions')
        data['description'] = data.pop('desc')
        answer['categories'].append({'info': data, 'points': answers_list.count(index), })
    return [answer]


def create_test_result():
    CustomUser.objects.create(email='admin')
    user_id = CustomUser.objects.all().last()
    created_date = timezone.now()
    result_id = TestResult.objects.create(results=RESULTS, user_id=user_id, created_date=created_date).id
    return result_id, created_date, user_id, str(TestResult.objects.get(id=result_id))


class DecodeResultTestCase(TestCase):
    fixtures = ['klimovcategory.json', ]

    def test_decode_result(self):
        result_id, created_date, user_id, url = create_test_result()
        test_answer = [decode_result(result) for result in TestResult.objects.all()]
        answer = get_answer(result_id, created_date, url)
        self.assertEqual(answer, test_answer)


class GetDecodedUserResultsTestCase(TestCase):
    fixtures = ['klimovcategory.json', ]

    def test_get_decoded_user_results(self):
        result_id, created_date, user_id, url = create_test_result()
        test_answer = get_decoded_user_results(user_id)
        answer = get_answer(result_id, created_date, url)
        self.assertEqual(answer, test_answer)


class MakeTopNResultsTestCase(TestCase):
    fixtures = ['klimovcategory.json', ]

    def test_decode_result(self):
        result_id, created_date, user_id, url = create_test_result()
        test_answer = get_decoded_user_results(user_id)
        make_top_n_results(test_answer)
        answer = [
            {'categories':
                 [{'info':
                       {'name': 'Людина - природа',
                        'examples': "Ландшафтний дизайнер, Фотограф, Кінолог, Ветеринар, Агроном, Еколог, Технолог"
                                    " харчової промисловості.",
                        'description': "Сфера діяльності даного типу спрямована на навколишнє нас природу. Це такі "
                                       "професії як ветеринар, еколог, агроном, геолог, мікробіолог. Професійно "
                                       "важливими якостями даних професій є: інтуїція, емпатія, вміння піклуватися "
                                       "про кого-небудь крім себе. Такі люди зазвичай трепетно ставляться до "
                                       "представників живої природи. Для успішної діяльності в професіях цього типу "
                                       "недостатньо просто бути любителем відпочинку на природі, важливо ще захищати "
                                       "природу, прагнути позитивно взаємодіяти з нею."}, 'points': 4},
                  {'info':
                       {'name': 'Людина - техніка',
                        'examples': 'Автомеханік, Інженер, Електрик, Пілот.',
                        'description': "Професії даного типу спрямовані на експлуатацію різних технічних пристроїв і "
                                       "приладів, їх обслуговування та створення. До таких професій належать: металург,"
                                       " водії різного транспорту, пілоти, слюсарі, технологи на підприємствах, "
                                       "будівельники, автомеханіки і т.д. Для їх успішної діяльності вкрай важливі "
                                       "технічний склад розуму, уважність, схильність до дій, а не роздумів."},
                   'points': 4},
                  {'info':
                       {'name': "Людина - людина",
                        'examples': "Психолог, SMM-менеджер, Інтернет-маркетолог, Project-менеджер, Маркетинг, "
                                    "Управління.",
                        'description': "До цього типу належать професії, основний напрямок яких пов'язано зі "
                                       "спілкуванням між людьми і їх взаємний вплив. Такі як, доктор, викладач, "
                                       "менеджер, учитель, психолог, продавець, тренер. Важливим якістю в даних "
                                       "професіях є не тільки бажання, але й вміння активної взаємодії з людьми і "
                                       "продуктивного спілкування. Важливою специфікою при підготовці є добрі знання "
                                       "професійної сфери і розвинені комунікативні навички."},
                   'points': 4}], 'date': created_date, 'id': result_id, 'url': url}]

        self.assertEqual(answer, test_answer)


class GenProfCategoriesTestCase(TestCase):
    fixtures = ['klimovcategory.json', ]

    def test_gen_prof_categories(self):
        answer = {
            0: {
                'name': 'Людина - природа',
                'examples': "Ландшафтний дизайнер, Фотограф, Кінолог, Ветеринар, Агроном, Еколог, Технолог харчової "
                            "промисловості.",
                'description': "Сфера діяльності даного типу спрямована на навколишнє нас природу. Це такі професії як "
                               "ветеринар, еколог, агроном, геолог, мікробіолог. Професійно важливими якостями даних "
                               "професій є: інтуїція, емпатія, вміння піклуватися про кого-небудь крім себе. Такі люди "
                               "зазвичай трепетно ставляться до представників живої природи. Для успішної діяльності в "
                               "професіях цього типу недостатньо просто бути любителем відпочинку на природі, важливо "
                               "ще захищати природу, прагнути позитивно взаємодіяти з нею."
            },

            1: {
                'name': 'Людина - техніка',
                'examples': "Автомеханік, Інженер, Електрик, Пілот.",
                'description': "Професії даного типу спрямовані на експлуатацію різних технічних пристроїв і приладів, "
                               "їх обслуговування та створення. До таких професій належать: металург, водії різного "
                               "транспорту, пілоти, слюсарі, технологи на підприємствах, будівельники, автомеханіки і "
                               "т.д. Для їх успішної діяльності вкрай важливі технічний склад розуму, уважність, "
                               "схильність до дій, а не роздумів."
            },

            2: {
                'name': 'Людина - людина',
                'examples': "Психолог, SMM-менеджер, Інтернет-маркетолог, Project-менеджер, Маркетинг, Управління.",
                'description': "До цього типу належать професії, основний напрямок яких пов'язано зі спілкуванням між "
                               "людьми і їх взаємний вплив. Такі як, доктор, викладач, менеджер, учитель, психолог, "
                               "продавець, тренер. Важливим якістю в даних професіях є не тільки бажання, але й вміння "
                               "активної взаємодії з людьми і продуктивного спілкування. Важливою специфікою при "
                               "підготовці є добрі знання професійної сфери і розвинені комунікативні навички."
            },

            3: {
                'name': 'Людина - знакова система',
                'examples': "Data Science, Програміст Python, Розробник мобільних додатків, Інтернет-маркетолог.",
                'description': "Основним напрямком діяльності даного типу професій є робота з цифрами, формулами, "
                               "розрахунками, текстами, базами даних. Це такі професії як програміст, економіст, "
                               "редактор, аналітик, перекладач, датасайнтіст, бухгалтер. Професійно важливі якості "
                               "даного типу професій: точність і аналітичний склад розуму, уважність, логічне мислення."
                               " Для успішної діяльності важливо мати інтерес до різних формулам, таблицям, картам, "
                               "схемами, баз даних."
            },

            4: {
                'name': 'Людина - художній образ',
                'examples': "Дизайнер, Кліпмейкер, Кіноактор, ТВ - Байєр.",
                'description': "Професії даного типу підходять людям з розвиненим образним мисленням і творчою жилкою. "
                               "Фахівці працюють в напрямку «людина - художній образ», обдаровані талантом або мають "
                               "покликання до цього з малих років. Їх діяльність пов'язана з проектуванням, створенням,"
                               " моделюванням, виготовленням різних творів мистецтва."
            },
        }
        test_answer = gen_prof_categories()
        self.assertEqual(answer, test_answer)
