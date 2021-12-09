from modeltranslation.translator import register, TranslationOptions
from .models import City, Region, StudyField, Speciality, University


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(StudyField)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Speciality)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(University)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)
