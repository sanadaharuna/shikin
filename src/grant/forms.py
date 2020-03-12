from django import forms


class GrantSearchForm(forms.Form):
    foundation = forms.CharField(label="財団等の名称", required=False)
    grant_name = forms.CharField(label="公募名", required=False)
