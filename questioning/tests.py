from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.utils import timezone
from questioning.cron import remove_obsolete_records
from questioning.models import TestResult, KlimovCategory, ConnectionKlimovCatStudyField, ConnectionInterestCatSpec
from questioning.services import save_questioning_results, generate_result, gen_results, get_top_categories, \
    _gen_result, get_generated_user_results, get_top_n_results, get_prof_categories, get_fields_links, \
    get_question_type, get_button_styles, delete_result, get_result
from users.models import CustomUser

RESULTS = {'1': 4, '2': 4, '3': 4, '4': 4, '5': 4}


class QuestioningTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_questioning(self):
        response = self.client.get('/questioning/')
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed('questioning.html'):
            render_to_string('questioning.html')

    def test_questioning_ajax(self):
        response = self.client.get('/questioning/')
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed('questioning_ajax.html'):
            render_to_string('questioning_ajax.html')


class GetFieldsLinksTest(TestCase):
    def test_get_fields_links_1(self):
        item = 1
        study_fields = ConnectionKlimovCatStudyField.objects.select_related('field_id').all()
        fields = get_fields_links(study_fields, item, 1)
        test_fields = [['Посилання на пошук:', '']]
        self.assertEqual(test_fields, fields)

    def test_get_fields_links_3(self):
        item = 1
        study_fields = ConnectionInterestCatSpec.objects.select_related('spec_id').all()
        fields = get_fields_links(study_fields, item, 3)
        test_fields = [['Посилання на пошук:', '']]
        self.assertEqual(test_fields, fields)


class GetQuestionTypeNameTest(TestCase):
    def test_get_question_type_name_1(self):
        fields = get_question_type(1)
        test_fields = "Тест на визначення профорієнтації"
        self.assertEqual(test_fields, fields)

    def test_get_question_type_name_3(self):
        fields = get_question_type(3)
        test_fields = "Тест на визначення типу майбутньої професії"
        self.assertEqual(test_fields, fields)


class GetButtonStylesTest(TestCase):
    def test_get_button_styles_1(self):
        fields = get_button_styles(1)
        test_fields = ['btn btn-primary', 'btn btn-info']
        self.assertEqual(test_fields, fields)

    def test_get_button_styles_2(self):
        fields = get_button_styles(2)
        test_fields = ['btn btn-primary', 'btn btn-secondary', 'btn btn-danger']
        self.assertEqual(test_fields, fields)

    def test_get_button_styles_3(self):
        fields = get_button_styles(3)
        test_fields = ['btn btn-primary', 'btn btn-info', 'btn btn-secondary', 'btn btn-warning', 'btn btn-danger']
        self.assertEqual(test_fields, fields)


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
        save_questioning_results(user_id=self.user_id, results=RESULTS, test_type=1)
        self.assertEqual(len(TestResult.objects.all()), 1)


class DeleteResultTestCase(TestCase):
    def test_delete_result_1(self):
        result_id, created_date, user_id, url = create_test_result()
        self.assertEqual(len(TestResult.objects.all()), 1)
        delete_result(result_id + 1, user_id)
        self.assertEqual(len(TestResult.objects.all()), 1)

    def test_delete_result_2(self):
        result_id, created_date, user_id, url = create_test_result()
        self.assertEqual(len(TestResult.objects.all()), 1)
        delete_result(result_id, user_id.id - 1)
        self.assertEqual(len(TestResult.objects.all()), 1)

    def test_delete_result_3(self):
        result_id, created_date, user_id, url = create_test_result()
        self.assertEqual(len(TestResult.objects.all()), 1)
        delete_result(result_id, user_id)
        self.assertEqual(len(TestResult.objects.all()), 0)


class GenResultTestCase(TestCase):
    fixtures = ['klimovcategory.json', 'studyfields.json', 'specialities.json', 'connection.json']

    def test_gen_result(self):
        test_answer = {'title': "Ваші результати:",
                       'data': [{'categories': [{
                           "name": 'Професії типу «Людина - природа» - середньо виражена схильність (4 з 8 балів).',
                           "desc": "Сфера діяльності даного типу спрямована на навколишнє нас природу. Це такі професії"
                                   " як ветеринар, еколог, агроном, геолог, мікробіолог. Професійно важливими якостями"
                                   " даних професій є: інтуїція, емпатія, вміння піклуватися про кого-небудь крім себе."
                                   " Такі люди зазвичай трепетно ставляться до представників живої природи. Для "
                                   "успішної діяльності в професіях цього типу недостатньо просто бути любителем "
                                   "відпочинку на природі, важливо ще захищати природу, прагнути позитивно взаємодіяти"
                                   " з нею.",
                           "prof": ["Ландшафтний дизайнер, Фотограф, Кінолог, Ветеринар, Агроном, Еколог, Технолог "
                                    "харчової промисловості."],
                           "study_fields": [['Посилання на пошук:', ''], ['09 Біологія', '09_Біологія'],
                                            ['10 Природничі науки', '10_Природничі_науки'],
                                            ['16 Хімічна та біоінженерія', '16_Хімічна_та_біоінженерія'],
                                            ['20 Аграрні науки та продовольство',
                                             '20_Аграрні_науки_та_продовольство'],
                                            ['21 Ветеринарна медицина', '21_Ветеринарна_медицина'],
                                            ['22 Охорона здоров’я', '22_Охорона_здоров’я']], 'id': 'cat_0'},
                           {
                               "name": 'Професії типу «Людина - техніка» - середньо виражена схильність (4 з 8 балів).',
                               "desc": "Професії даного типу спрямовані на експлуатацію різних технічних пристроїв "
                                       "і приладів, їх обслуговування та створення. До таких професій належать: "
                                       "металург, водії різного транспорту, пілоти, слюсарі, технологи на підприємствах"
                                       ", будівельники, автомеханіки і т.д. Для їх успішної діяльності вкрай важливі "
                                       "технічний склад розуму, уважність, схильність до дій, а не роздумів.",
                               "prof": ["Автомеханік, Інженер, Електрик, Пілот."],
                               "study_fields": [['Посилання на пошук:', ''],
                                                ['13 Механічна інженерія', '13_Механічна_інженерія'],
                                                ['14 Електрична інженерія', '14_Електрична_інженерія'],
                                                ['15 Автоматизація та приладобудування',
                                                 '15_Автоматизація_та_приладобудування'],
                                                ['17 Електроніка та телекомунікації',
                                                 '17_Електроніка_та_телекомунікації'],
                                                ['18 Виробництво та технології', '18_Виробництво_та_технології'],
                                                ['27 Транспорт', '27_Транспорт']], 'id': 'cat_1'},
                           {
                               "name": 'Професії типу «Людина - людина» - середньо виражена схильність (4 з 8 балів).',
                               "desc": "До цього типу належать професії, основний напрямок яких пов'язано зі "
                                       "спілкуванням між людьми і їх взаємний вплив. Такі як, доктор, викладач, "
                                       "менеджер, учитель, психолог, продавець, тренер. Важливим якістю в даних "
                                       "професіях є не тільки бажання, але й вміння активної взаємодії з людьми і "
                                       "продуктивного спілкування. Важливою специфікою при підготовці є добрі "
                                       "знання професійної сфери і розвинені комунікативні навички.",
                               "prof": ["Психолог, SMM-менеджер, Інтернет-маркетолог, Project-менеджер, Маркетинг,"
                                        " Управління."],
                               "study_fields": [['Посилання на пошук:', ''], ['01 Освіта', '01_Освіта'],
                                                ['03 Гуманітарні науки', '03_Гуманітарні_науки'],
                                                ['04 Богослов’я', '04_Богослов’я'],
                                                ['05 Соціальні та поведінкові науки',
                                                 '05_Соціальні_та_поведінкові_науки'],
                                                ['06 Журналістика', '06_Журналістика'],
                                                ['07 Управління та адміністрування',
                                                 '07_Управління_та_адміністрування'],
                                                ['08 Право', '08_Право'],
                                                ['23 Соціальна робота', '23_Соціальна_робота'],
                                                ['24 Сфера обслуговування', '24_Сфера_обслуговування'],
                                                ['25 Воєнні науки, національна безпека, безпека державного кордону',
                                                 '25_Воєнні_науки,_національна_безпека,_безпека_державного_кордону'],
                                                ['26 Цивільна безпека', '26_Цивільна_безпека'],
                                                ['28 Публічне управління і адміністрування',
                                                 '28_Публічне_управління_і_адміністрування'],
                                                ['29 Міжнародні відносини', '29_Міжнародні_відносини']], 'id': 'cat_2'}
                       ]}]}
        answer = generate_result(RESULTS)
        self.assertEqual(answer, test_answer)


class GenResultsTestCase(TestCase):
    fixtures = ['klimovcategory.json', 'studyfields.json', 'specialities.json', 'connection.json']

    def test_gen_results(self):
        url = '72f126da7df6798cd22c5bb5d6aab5d7'
        result_id = 42
        q_type = 1
        test_answer = [{'date': timezone.now().strftime("%d/%m/%Y"),
                        'categories': [{'name': 'Людина - природа',
                                        'prof':
                                            ['Ландшафтний дизайнер', ' Фотограф', ' Кінолог', ' Ветеринар', ' Агроном',
                                             ' Еколог', ' Технолог харчової промисловості'],
                                        'study_fields':
                                            [['Посилання на пошук:', ''], ['09 Біологія', '09_Біологія'],
                                             ['10 Природничі науки', '10_Природничі_науки'],
                                             ['16 Хімічна та біоінженерія', '16_Хімічна_та_біоінженерія'],
                                             ['20 Аграрні науки та продовольство', '20_Аграрні_науки_та_продовольство'],
                                             ['21 Ветеринарна медицина', '21_Ветеринарна_медицина'],
                                             ['22 Охорона здоров’я', '22_Охорона_здоров’я']],
                                        'id': 'cat_1_0'},
                                       {'name': 'Людина - техніка',
                                        'prof': ['Автомеханік', ' Інженер',
                                                 ' Електрик',
                                                 ' Пілот'], 'study_fields': [
                                           ['Посилання на пошук:', ''],
                                           ['13 Механічна інженерія', '13_Механічна_інженерія'],
                                           ['14 Електрична інженерія', '14_Електрична_інженерія'],
                                           ['15 Автоматизація та приладобудування',
                                            '15_Автоматизація_та_приладобудування'],
                                           ['17 Електроніка та телекомунікації', '17_Електроніка_та_телекомунікації'],
                                           ['18 Виробництво та технології', '18_Виробництво_та_технології'],
                                           ['27 Транспорт', '27_Транспорт']],
                                        'id': 'cat_2_0'},
                                       {'name': 'Людина - людина',
                                        'prof': ['Психолог', ' SMM-менеджер',
                                                 ' Інтернет-маркетолог', ' Project-менеджер',
                                                 ' Маркетинг', ' Управління'],
                                        'study_fields': [['Посилання на пошук:', ''],
                                                         ['01 Освіта', '01_Освіта'],
                                                         ['03 Гуманітарні науки', '03_Гуманітарні_науки'],
                                                         ['04 Богослов’я', '04_Богослов’я'],
                                                         ['05 Соціальні та поведінкові науки',
                                                          '05_Соціальні_та_поведінкові_науки'],
                                                         ['06 Журналістика', '06_Журналістика'],
                                                         ['07 Управління та адміністрування',
                                                          '07_Управління_та_адміністрування'],
                                                         ['08 Право', '08_Право'],
                                                         ['23 Соціальна робота', '23_Соціальна_робота'],
                                                         ['24 Сфера обслуговування', '24_Сфера_обслуговування'], [
                                                             '25 Воєнні науки, національна безпека, безпека державного кордону',
                                                             '25_Воєнні_науки,_національна_безпека,_безпека_державного_кордону'],
                                                         ['26 Цивільна безпека',
                                                          '26_Цивільна_безпека'], [
                                                             '28 Публічне управління і адміністрування',
                                                             '28_Публічне_управління_і_адміністрування'],
                                                         ['29 Міжнародні відносини',
                                                          '29_Міжнародні_відносини']],
                                        'id': 'cat_3_0'}], 'id': 42,
                        'url': '72f126da7df6798cd22c5bb5d6aab5d7', 'type': 'Тест на визначення профорієнтації',
                        'short': 1}]

        answer = gen_results(
            [{'results': str(RESULTS), 'created_date': timezone.now(), 'url': url, 'id': result_id, 'type': q_type}])
        self.assertEqual(answer, test_answer)


class GetResultTestCase(TestCase):
    fixtures = ['klimovcategory.json', 'studyfields.json', 'specialities.json', 'connection.json']

    def test_get_result1(self):
        user_id = CustomUser.objects.create(email='admin')
        test_answer = {'title': 'Ви не пройшли опитування', }
        answer = get_result(user=user_id)
        self.assertEqual(answer, test_answer)

    def test_gen_result2(self):
        user_id = CustomUser.objects.create(email='admin')
        result_id = TestResult.objects.create(results=RESULTS, user_id=user_id).id
        url = TestResult.objects.get(id=result_id).url
        q_type = 1
        items = gen_results(
            [{'results': str(RESULTS), 'created_date': timezone.now(), 'url': url, 'id': result_id, 'type': q_type}])
        test_answer = {'title': 'Ваші результати', 'data': items}
        answer = get_result(user=user_id)
        self.assertEqual(answer, test_answer)


class GetTopCategoriesTestCase(TestCase):
    def test_get_top_categories(self):
        test_answer = {'1': 4, '2': 4, '3': 4}
        answer = get_top_categories(RESULTS)
        self.assertEqual(answer, test_answer)


def get_answer(result_id, created_date, url):
    answers_list = RESULTS
    answer = {'categories': [], 'date': created_date, 'id': result_id, 'url': url}
    klimov_category_list = list(KlimovCategory.objects.all().values('name', 'professions', 'desc'))
    for data in klimov_category_list:
        index = klimov_category_list.index(data)
        data['name'] = f"Людина - {data['name']}"
        data['examples'] = data.pop('professions')
        data['description'] = data.pop('desc')
        answer['categories'].append({'info': data, 'points': answers_list[str(index+1)],'max_points': 8 })
    return [answer]


def create_test_result(results_cur=RESULTS, q_type=1, email='admin'):
    CustomUser.objects.create(email=email)
    user_id = CustomUser.objects.all().last()
    created_date = timezone.now()
    result_id = TestResult.objects.create(results=results_cur, user_id=user_id, created_date=created_date,
                                          type=q_type).id
    return result_id, created_date, user_id, str(TestResult.objects.get(id=result_id))


class DecodeResultTestCase(TestCase):
    fixtures = ['klimovcategory.json', 'studyfields.json', 'specialities.json', 'connection.json']

    def test_decode_result(self):
        result_id, created_date, user_id, url = create_test_result()
        test_answer = [_gen_result(result) for result in TestResult.objects.all()]
        answer = get_answer(result_id, created_date, url)
        self.assertEqual(answer, test_answer)


class GetGeneratedUserResultsTestCase(TestCase):
    fixtures = ['klimovcategory.json', 'studyfields.json', 'specialities.json', 'connection.json']

    def test_get_generated_user_results(self):
        result_id, created_date, user_id, url = create_test_result()
        test_answer = get_generated_user_results(user_id)
        answer = get_answer(result_id, created_date, url)
        self.assertEqual(answer, test_answer)


class GetTopNResultsTestCase(TestCase):
    fixtures = ['klimovcategory.json', 'studyfields.json', 'specialities.json', 'connection.json', 'interests.json']

    def test_get_top_n_results_1(self):
        cur_results = {'1': 4, '2': 6, '3': 6, '4': 2, '5': 3}
        result_id, created_date, user_id, url = create_test_result(cur_results)
        test_answer = get_generated_user_results(user_id)
        test_answer=get_top_n_results(test_answer)
        answer = [
            {'categories':
                 [{'info':
                       {'name': 'Людина - техніка',
                        'examples': 'Автомеханік, Інженер, Електрик, Пілот.',
                        'description': "Професії даного типу спрямовані на експлуатацію різних технічних пристроїв і "
                                       "приладів, їх обслуговування та створення. До таких професій належать: металург,"
                                       " водії різного транспорту, пілоти, слюсарі, технологи на підприємствах, "
                                       "будівельники, автомеханіки і т.д. Для їх успішної діяльності вкрай важливі "
                                       "технічний склад розуму, уважність, схильність до дій, а не роздумів."},
                   'points': 6, 'max_points': 8},
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
                   'points': 6, 'max_points': 8},
                  {'info':
                       {'name': 'Людина - природа',
                        'examples': "Ландшафтний дизайнер, Фотограф, Кінолог, Ветеринар, Агроном, Еколог, Технолог"
                                    " харчової промисловості.",
                        'description': "Сфера діяльності даного типу спрямована на навколишнє нас природу. Це такі "
                                       "професії як ветеринар, еколог, агроном, геолог, мікробіолог. Професійно "
                                       "важливими якостями даних професій є: інтуїція, емпатія, вміння піклуватися "
                                       "про кого-небудь крім себе. Такі люди зазвичай трепетно ставляться до "
                                       "представників живої природи. Для успішної діяльності в професіях цього типу "
                                       "недостатньо просто бути любителем відпочинку на природі, важливо ще захищати "
                                       "природу, прагнути позитивно взаємодіяти з нею."},
                   'points': 4, 'max_points': 8}
                  ], 'date': created_date, 'id': result_id, 'url': url}]
        self.assertEqual(answer, test_answer)

    def test_get_top_n_results_2(self):
        cur_results = {'1': 1, '2': 2, '3': 2, '4': 3, '5': 3, '6': 2, '7': 2, '8': 2, '9': 3, '10': 2, '11': 2,
                       '12': 3, '13': 30, '14': 20, '15': 10, '16': 3, '17': 5, '18': 2, '19': 0}
        result_id, created_date, user_id, url = create_test_result(cur_results, 3, 'sadasdsa')
        test_answer = get_generated_user_results(user_id)
        test_answer=get_top_n_results(test_answer)
        answer = [
            {'categories':
                 [{'info':
                       {'name': 'Право, юриспруденція',
                        'examples': 'адвокат, нотаріус, юрист, прокурор, колектор, слідчий, суддя, приватний детектив,'
                                    ' експерт – криміналіст.',
                        'description': 'У вас гарне ораторське мистецтво, ви чудово володіє навичками листа, знаєте '
                                       'закони і вмієте вирішувати складні питання. Тоді ви зможете чудово реалізувати '
                                       'себе в галузі юриспруденції. Для вступу необхідно здати історію, '
                                       'суспільствознавство чи англійську мову.'},
                   'points': 30, 'max_points': 12},
                  {'info':
                       {'name': "Сфера обслуговування, торгівля",
                        'examples': "перукар, продавець, мерчендайзер, кухар, менеджер з продажу, товарознавець, "
                                    "супервайзер, трейдер, дистриб'ютор, гід, візажист, ріелтор, стиліст, швачка.",
                        'description': 'Відмінні знання про суспільствознавство можуть привести вас у сферу послуг та'
                                       ' торгівлі. Тут ви зможете реалізувати свій творчий потенціал у взаємодії'
                                       ' із людьми.'}, 'points': 20, 'max_points': 12},
                  {'info':
                       {'name': 'Економіка та фінанси',
                        'examples': 'Аналітик, страховий агент, банківський службовець, бухгалтер, скарбник, контролер,'
                                    ' податковий інспектор, фінансист.',
                        'description': "Якщо вам у школі вам цікаві такі предмети як математика та "
                                       "суспільствознавство, то надалі ви зможете пов'язати свою професію з "
                                       "економічною діяльністю. Ця галузь активно розвивається і не стоїть на місці, "
                                       "тому ви ніколи не залишитеся без роботи."},
                   'points': 10, 'max_points': 12}
                  ], 'date': created_date, 'id': result_id, 'url': url}]
        self.assertEqual(answer, test_answer)


class GetProfCategoriesTestCase(TestCase):
    fixtures = ['klimovcategory.json', 'studyfields.json', 'specialities.json', 'connection.json']

    def test_get_prof_categories(self):
        answer = {
            1: {
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
            2: {
                'name': 'Людина - техніка',
                'examples': "Автомеханік, Інженер, Електрик, Пілот.",
                'description': "Професії даного типу спрямовані на експлуатацію різних технічних пристроїв і приладів, "
                               "їх обслуговування та створення. До таких професій належать: металург, водії різного "
                               "транспорту, пілоти, слюсарі, технологи на підприємствах, будівельники, автомеханіки і "
                               "т.д. Для їх успішної діяльності вкрай важливі технічний склад розуму, уважність, "
                               "схильність до дій, а не роздумів."
            },
            3: {
                'name': 'Людина - людина',
                'examples': "Психолог, SMM-менеджер, Інтернет-маркетолог, Project-менеджер, Маркетинг, Управління.",
                'description': "До цього типу належать професії, основний напрямок яких пов'язано зі спілкуванням між "
                               "людьми і їх взаємний вплив. Такі як, доктор, викладач, менеджер, учитель, психолог, "
                               "продавець, тренер. Важливим якістю в даних професіях є не тільки бажання, але й вміння "
                               "активної взаємодії з людьми і продуктивного спілкування. Важливою специфікою при "
                               "підготовці є добрі знання професійної сфери і розвинені комунікативні навички."
            },
            4: {
                'name': 'Людина - знакова система',
                'examples': "Data Science, Програміст Python, Розробник мобільних додатків, Інтернет-маркетолог.",
                'description': "Основним напрямком діяльності даного типу професій є робота з цифрами, формулами, "
                               "розрахунками, текстами, базами даних. Це такі професії як програміст, економіст, "
                               "редактор, аналітик, перекладач, датасайнтіст, бухгалтер. Професійно важливі якості "
                               "даного типу професій: точність і аналітичний склад розуму, уважність, логічне мислення."
                               " Для успішної діяльності важливо мати інтерес до різних формулам, таблицям, картам, "
                               "схемами, баз даних."
            },
            5: {
                'name': 'Людина - художній образ',
                'examples': "Дизайнер, Кліпмейкер, Кіноактор, ТВ - Байєр.",
                'description': "Професії даного типу підходять людям з розвиненим образним мисленням і творчою жилкою. "
                               "Фахівці працюють в напрямку «людина - художній образ», обдаровані талантом або мають "
                               "покликання до цього з малих років. Їх діяльність пов'язана з проектуванням, створенням,"
                               " моделюванням, виготовленням різних творів мистецтва."
            },
        }
        test_answer = get_prof_categories(1)
        self.assertEqual(answer, test_answer)
