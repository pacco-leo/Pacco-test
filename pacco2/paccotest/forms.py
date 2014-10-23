from django import forms
from paccotest.models import Survey

class GPSMeasureForm(forms.ModelForm):

    class Meta:
        model = Survey

    def __init__(self, user, *args, **kwargs):
        super(GPSMeasureForm, self).__init__(*args, **kwargs)
        self.fields['latitude'].widget = forms.HiddenInput()
        self.fields['longitude'].widget = forms.HiddenInput()
        self.fields['elevation'].widget = forms.HiddenInput()
        self.fields['utc'].widget = forms.HiddenInput()
