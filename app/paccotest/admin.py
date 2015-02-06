from django.contrib import admin
from models import Question, Answer, Survey, UserAnswer, Probe, ProbeMeasure, PlateformInfo

class QuestionAdmin(admin.ModelAdmin):
	def get_form(self, request, obj=None, **kwargs):
		self.exclude = []
		if not request.user.is_superuser:
			self.exclude.append('text')
			self.exclude.append('text_fr')
			self.exclude.append('text_nl')
			self.exclude.append('text_en')
		return super(QuestionAdmin, self).get_form(request, obj, **kwargs)

class AnswerAdmin(admin.ModelAdmin):
	def get_form(self, request, obj=None, **kwargs):
		self.exclude = []
		if not request.user.is_superuser:
			self.exclude.append('text')
			self.exclude.append('text_fr')
			self.exclude.append('text_nl')
			self.exclude.append('text_en')
		return super(AnswerAdmin, self).get_form(request, obj, **kwargs)

# Register your models here.
admin.site.register(PlateformInfo)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Probe)

# User values
admin.site.register(Survey)
admin.site.register(UserAnswer)
admin.site.register(ProbeMeasure)

