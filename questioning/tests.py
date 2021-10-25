from django.test import TestCase
from django.utils import timezone
from questioning.cron import remove_obsolete_records
from questioning.models import TestResult
from questioning.services import save_questions_results, gen_result
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
                                 "харчової промисловості...",
            'second_professions': "Ви можете почати освоювати одну з відповідних вам професій:\n"
                                  "Автомеханік, Інженер, Електрик, Пілот...",
            'third_professions': "Ви можете почати освоювати одну з відповідних вам професій:\n"
                                 "Психолог, SMM-менеджер, Інтернет-маркетолог, Project-менеджер, Маркетинг, Управління"
                                 "...",
            'first_result': 'Професії типу «Людина - природа» - середньо виражена схильність (4 з 8 балів).',
            'second_result': 'Професії типу «Людина - техніка» - середньо виражена схильність (4 з 8 балів).',
            'third_result': 'Професії типу «Людина - людина» - середньо виражена схильність (4 з 8 балів).',
        }
        answer = gen_result(eval(RESULTS))
        self.assertEqual(answer, test_answer)
