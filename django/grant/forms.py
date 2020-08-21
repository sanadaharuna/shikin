from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms
from django.urls import reverse

from grant.models import Grant


class GrantForm(forms.ModelForm):
    class Meta:
        model = Grant
        fields = ["accepted_at", "zaidanmei",
                  "koubomei", "url", "torimatome", "bikou"]
        widgets = {"accepted_at": DatePickerInput(format='%Y-%m-%d')}

    def __init__(self, *args, **kwargs):
        super(GrantForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit("", "保存"))


class GrantSearchForm(forms.Form):
    q = forms.CharField(label="助成財団等の名称、公募名", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('q'),
        )
        self.helper.form_method = "GET"
        self.helper.form_action = reverse("grant:list")
        self.helper.add_input(Submit("", "絞り込み"))
