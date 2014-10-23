from django import forms
from paccotest.models import Survey

class GPSMeasureForm(forms.ModelForm):
    #Will override the utc from Survey Model
    #Needed to specify Date Format
    #utc = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'), input_formats=('%d/%m/%Y',))

    class Meta:
        model = Survey
        #exclude = ('utc',)

    def __init__(self, *args, **kwargs):
        super(GPSMeasureForm, self).__init__(*args, **kwargs)

        print args
        self.fields['latitude'].widget = forms.HiddenInput()
        self.fields['longitude'].widget = forms.HiddenInput()
        self.fields['elevation'].widget = forms.HiddenInput()
        self.fields['utc'].widget = forms.HiddenInput()
