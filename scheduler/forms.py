from django import forms
from django.forms import ModelForm, SelectDateWidget
from django.core.exceptions import ValidationError

from scheduler.models.company_m import CompanyInfo
from scheduler.string_name import NAME, FIELD, TERM, DATE


class CompanyForm(ModelForm):
    class Meta:
        company = forms.CharField(required=True)
        field_of = forms.CharField(required=True)
        term = forms.IntegerField(required=True)
        date = forms.DateField(widget=SelectDateWidget(years=range(2025, 1939, -1)))
        sheet_name = forms.CharField(required=True)
        model = CompanyInfo
        fields = [NAME, FIELD, TERM, DATE, "sheet_name"]

        help_texts = {
            'name': '학교 이름을 입력하세요.',
            'field': "전공을 입력하세요",
            'term': "학기를 입력하세요.",
            'date': "날짜를 입력하세요.",
            'sheet name': "공유한 시트이름을 입력하세요"
        }
        error_messages = {
            'name': {
                'max_length': "This company's name is too long.",
            },
        }
