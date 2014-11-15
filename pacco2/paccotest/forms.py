from django import forms
from paccotest.models import Survey, Answer, Question, ProbeMeasure
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory

class GPSMeasureForm(forms.ModelForm):
    #Will override the utc from Survey Model
    #Needed to specify Date Format
    #utc = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'), input_formats=('%d/%m/%Y',))

    class Meta:
        model = Survey
        fields = ['latitude', 'longitude', 'elevation', 'utc', ]
        #exclude = ('utc',)

    def __init__(self, *args, **kwargs):
        super(GPSMeasureForm, self).__init__(*args, **kwargs)

        self.fields['latitude'].widget = forms.HiddenInput()
        self.fields['longitude'].widget = forms.HiddenInput()
        self.fields['elevation'].widget = forms.HiddenInput()
        self.fields['utc'].widget = forms.HiddenInput()

class ProbeMeasureForm(forms.ModelForm):

    class Meta:
        model = ProbeMeasure
        fields = ['probeType', 'measure',]

    def __init__(self, *args, **kwargs):
        super(ProbeMeasureForm, self).__init__(*args, **kwargs)

        self.fields['probeType'].widget = forms.HiddenInput()
        self.fields['measure'].widget = forms.HiddenInput()
#

# UserAnswerFormSet = formset_factory(UserAnswerForm)
# formset = UserAnswerFormSet()
# for form in foclass UserAnswerForm(forms.Form)
#     question_id = forms.IntegerField()
#     answer_id = forms.IntegerField()rmset:
#     print(form.as_table())
#    inlineformset_factory(Answer, Question.answers.through)

# class QuestionForm(forms.ModelForm):
#
#     #http://mounirmesselmeni.github.io/2013/11/25/django-grouped-select-field/
#
#      answers = forms.ModelChoiceField(Answer.objects.all(), widget=forms.RadioSelect)
#
#     #  category = GroupedModelChoiceField(
#     #     label=_('Category'),
#     #     group_by_field='parent',
#     #     queryset=Category.objects.all(),
#     # )
#
#
#
#      class Meta:
#          model = Question
#
#      def __init__(self, *args, **kwargs):
#          super(QuestionForm, self).__init__(*args, **kwargs)


# class QuestionForm(forms.ModelFor
#     #http://chase-seibert.github.io/blog/2010/05/20/django-manytomanyfield-on-modelform-as-checkbox-widget.html
#     #http://stackoverflow.com/questions/2216974/django-modelform-for-many-to-many-fields
#
#     class Meta:
#         model = Question
#         fields = ('question_text',)
#
#     # Representing the many to many related field in Pizza
#     answers = forms.ModelChoiceField(queryset=Answer.objects.all(),  widget=forms.RadioSelect)
#
#     # def __init__(self, *args, **kwargs):
#     #     super(QuestionForm, self).__init__(*args, **kwargs)
#     #
#     #     self.fields["answers"].widget = forms.CheckboxSelectMultiple()
#     #     self.fields["answers"].queryset = Answer.objects.all()m):