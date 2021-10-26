from django.contrib import admin
from .models import TestResult, QuestionsBase, KlimovCategory

admin.site.register(TestResult)
admin.site.register(QuestionsBase)
admin.site.register(KlimovCategory)
