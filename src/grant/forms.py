from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms
from grant.models import Grant


class GrantForm(forms.ModelForm):
    class Meta:
        model = Grant
        fields = "__all__"
        widgets = {
            "acceptance_date": DatePickerInput(
                format="%Y-%m-%d",
                options={"locale": "ja", "dayViewHeaderFormat": "YYYY年 MMMM"},
            )
        }

    def __init__(self, *args, **kwargs):
        super(GrantForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)


class GrantSearchForm(forms.Form):
    foundation = forms.CharField(label="財団等の名称", required=False)
    grant_name = forms.CharField(label="公募名", required=False)
