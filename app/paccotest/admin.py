from django.contrib import admin
from models import Question, Answer, Survey, UserAnswer, Probe, ProbeMeasure, PlateformInfo

# Register your models here.
admin.site.register(PlateformInfo)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Probe)

# User values
admin.site.register(Survey)
admin.site.register(UserAnswer)
admin.site.register(ProbeMeasure)
