from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from paccotest.models import Question

# Create your views here.

# Page of the survey
def survey(request):
    all_questions_list = Question.objects.all()
    context = {'all_questions': all_questions_list}
    return render(request, 'paccotest/survey.html', context)

##
# Page called when the survey is complete
def surveyComplete(request):
    return HttpResponseRedirect(reverse('paccotest:test'))

# Page of test
def test(request):
    return render(request, 'paccotest/test.html')



#See: http://stackoverflow.com/questions/14901680/how-to-do-a-multi-step-form-in-django
#https://www.youtube.com/watch?v=fSnBF-BmccQ
#https://docs.djangoproject.com/en/dev/ref/contrib/formtools/form-wizard/