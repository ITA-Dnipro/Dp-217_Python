from modeltranslation.translator import register, TranslationOptions
from .models import QuestionsBase, KlimovCategory, InterestCategory


@register(QuestionsBase)
class QuestionsBaseTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')


@register(KlimovCategory)
class KlimovCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'desc', 'professions')


@register(InterestCategory)
class InterestCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'desc', 'professions')
