from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from modeltranslation.admin import TranslationAdmin

from .models import TestResult, QuestionsBase, KlimovCategory, ConnectionKlimovCatStudyField, InterestCategory, \
    ConnectionInterestCatSpec


class QuestionsBaseAdminForm(forms.ModelForm):
    """Форма с виджетом ckeditor"""
    desc_ru = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    desc_en = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    desc_uk = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = QuestionsBase
        fields = '__all__'


class QuestionsBaseAdmin(TranslationAdmin):
    fields = ('question', 'answer')


class KlimovCategoryAdmin(TranslationAdmin):
    fields = ('name', 'desc', 'professions')


class InterestCategoryAdmin(TranslationAdmin):
    fields = ('name', 'desc', 'professions')


admin.site.register(TestResult)
admin.site.register(QuestionsBase)
admin.site.register(KlimovCategory)
admin.site.register(ConnectionKlimovCatStudyField)
admin.site.register(InterestCategory)
admin.site.register(ConnectionInterestCatSpec)
