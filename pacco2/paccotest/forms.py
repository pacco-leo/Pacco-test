from django import forms
from paccotest.models import GPSMeasure

class GPSMeasureForm(forms.ModelForm):

    class Meta:
        model = GPSMeasure

    def __init__(self, user, *args, **kwargs):
        super(GPSMeasureForm, self).__init__(*args, **kwargs)
        self.fields['latitude'].widget = forms.HiddenInput()
        self.fields['longitude'].widget = forms.HiddenInput()
        self.fields['survey'].widget = forms.HiddenInput()
