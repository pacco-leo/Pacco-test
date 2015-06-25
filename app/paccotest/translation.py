from modeltranslation.translator import translator, TranslationOptions
from models import Question, Answer, Probe, WaterCategorie

class QuestionTranslationOptions(TranslationOptions):
    fields = ('text',)

class AnswerTranslationOptions(TranslationOptions):
    fields = ('text',)

class ProbeTranslationOptions(TranslationOptions):
    fields = ('text',)

class ProbeTranslationOptions(TranslationOptions):
    fields = ('text',)

class WaterCategorieTranslationOptions(TranslationOptions):
    fields = ('text',)

translator.register(Question, QuestionTranslationOptions)
translator.register(Answer, AnswerTranslationOptions)
translator.register(Probe, ProbeTranslationOptions)
translator.register(WaterCategorie, WaterCategorieTranslationOptions)

