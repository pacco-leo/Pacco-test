from django.contrib import admin
from models import Question, Answer, Survey, UserAnswer, ProbeType, ProbeMeasure

# Register your models here.
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "answer_text")
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question)
admin.site.register(Survey)
admin.site.register(UserAnswer)
admin.site.register(ProbeType)
admin.site.register(ProbeMeasure)
