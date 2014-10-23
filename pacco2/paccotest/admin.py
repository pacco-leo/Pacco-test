from django.contrib import admin
from models import Question, Answer, Survey, UserAnswer, ProbeType, ProbeMeasure

# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Survey)
admin.site.register(UserAnswer)
admin.site.register(ProbeType)
admin.site.register(ProbeMeasure)
