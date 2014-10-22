from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from paccotest.models import Question

from django.contrib.formtools.wizard.views import SessionWizardView

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

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


class ContactWizard(SessionWizardView):
    logger.info("ContactWizard!")
    template_name = "paccotest/form.html"

    def done(self, form_list, **kwargs):

        logger.info("Done!")
        return render_to_response('paccotest/done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })

#See: http://stackoverflow.com/questions/14901680/how-to-do-a-multi-step-form-in-django
#https://www.youtube.com/watch?v=fSnBF-BmccQ
#https://docs.djangoproject.com/en/dev/ref/contrib/formtools/form-wizard/