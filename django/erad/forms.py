from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from erad.models import Item

FUNDING_AGENCY = (
    ("", "選択なし"),
    ("国立研究開発法人日本医療研究開発機構", "国立研究開発法人日本医療研究開発機構(AMED)"),
    ("国立研究開発法人情報通信研究機構", "国立研究開発法人情報通信研究機構(NICT)"),
    ("国立研究開発法人科学技術振興機構", "国立研究開発法人科学技術振興機構(JST)"),
    ("独立行政法人日本学術振興会", "独立行政法人日本学術振興会(JSPS)"),
    ("国立研究開発法人医薬基盤・健康・栄養研究所", "国立研究開発法人医薬基盤・健康・栄養研究所(NIBIOHN)"),
    ("国立研究開発法人農業・食品産業技術総合研究機構", "国立研究開発法人農業・食品産業技術総合研究機構(NARO)"),
    ("国立研究開発法人新エネルギー・産業技術総合開発機構", "国立研究開発法人新エネルギー・産業技術総合開発機構(NEDO)"),
    ("独立行政法人環境再生保全機構", "独立行政法人環境再生保全機構"),
    ("内閣府", "内閣府"),
    ("総務省", "総務省"),
    ("消防庁", "消防庁"),
    ("文部科学省", "文部科学省"),
    ("厚生労働省", "厚生労働省"),
    ("農林水産省", "農林水産省"),
    ("農林水産省農林水産政策研究所", "農林水産省農林水産政策研究所"),
    ("経済産業省", "経済産業省"),
    ("国土交通省", "国土交通省"),
    ("国土技術政策総合研究所", "国土技術政策総合研究所"),
    ("環境省", "環境省"),
    ("原子力規制庁", "原子力規制庁"),
    ("防衛省", "防衛省"),
)


class ItemSearchForm(forms.Form):
    funding_agency = forms.ChoiceField(
        label="配分機関", choices=FUNDING_AGENCY, required=False
    )
    call_for_applications = forms.CharField(label="公募名", required=False)
    before_closing_date = forms.BooleanField(
        label="受付終了日前の公募案件のみ表示する", required=False, initial="on"
    )


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            "id",
            "url",
            "publishing_date",
            "funding_agency",
            "call_for_applications",
            "application_unit",
            "approved_institution",
            "opening_date",
            "closing_date"
        ]
        widgets = {
            "publishing_date": DatePickerInput(format='%Y-%m-%d'),
            "opening_date": DatePickerInput(format='%Y-%m-%d'),
            "closing_date": DatePickerInput(format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("", "保存"))
