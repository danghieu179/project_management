from django import forms
from .utils.const import URL_GOOGLE_DRIVE


class SonarForm(forms.Form):
    url = forms.URLField(max_length=250, required=True,
                         initial=URL_GOOGLE_DRIVE)


class SonarFormInput(forms.Form):
    from_date = forms.DateField(required=True,)
    to_date = forms.DateField(required=True,)
    unit_test = forms.IntegerField(max_value=100, min_value=0, required=False)
    blocker = forms.IntegerField(required=False)
    critical = forms.IntegerField(required=False)
    major = forms.IntegerField(required=False)
    minor = forms.IntegerField(required=False)
    show_chart = forms.BooleanField(initial=True)

    def __init__(self, projects, *args, **kwargs):
        super(SonarFormInput, self).__init__(*args, **kwargs)
        self.fields['project'] = forms.CharField(
            widget=forms.Select(choices=projects))
