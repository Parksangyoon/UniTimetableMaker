import gspread
from django.shortcuts import redirect
from django.views.generic import ListView

from scheduler.db_manager import set_db_data
from scheduler.google_sheet import read_sheet
from scheduler.models.company_m import CompanyInfo
from scheduler.models.subject_m import SubjectInfo
from scheduler.string_name import COMPLETION_TYPE, SUBJECT_KEY_NAME, SHEET_SUBJECT, COMPANY
from ..tables import SubjectTable
from ..views.common_v import request_table_config


class SubjectListView(ListView):
    template_name = 'timetable/subject_t.html'
    model = SubjectInfo
    object_list = None

    def get_queryset(self):
        subject_list = SubjectInfo.objects.filter(company_id=self.kwargs['company_id'])
        if subject_list.__len__() is 0:
            get_subject_list(self.kwargs['company_id'])
        return subject_list

    def get(self, request, *args, **kwargs):

        self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)
        table = SubjectTable(self.object_list)
        request_table_config(request, table)
        context['table'] = table
        context['company_name'] = CompanyInfo.objects.get(id=self.kwargs['company_id']).name
        return self.render_to_response(context)


def update_subject(request, company_id):
    subject_list = SubjectInfo.objects.all()
    for subject in subject_list:
        subject.delete()
    get_subject_list(company_id)
    return redirect('subject_list', company_id=company_id)


# 시트에서 과목 데이터 가져오기
def get_subject_list(company_id):
    company_data = CompanyInfo.objects.get(id=company_id)
    try:
        sheet = read_sheet(company_data.sheet_name, "과목")
    except gspread.exceptions.SpreadsheetNotFound:
        return redirect('home')
    subject_of_sheet = sheet.get_all_records(head=1)
    subject_list = []
    subject = dict()
    for dict_data in subject_of_sheet:
        for data in dict_data.keys():
            if '이수구분' in data:
                subject[COMPLETION_TYPE] = SubjectInfo.Type.from_string(dict_data[data])
            else:
                subject[SUBJECT_KEY_NAME[SHEET_SUBJECT.index(data)]] = dict_data[data]
                subject[COMPANY] = company_data
        subject_list.append(subject)
        subject = dict()
    set_db_data(SubjectInfo, subject_list)
    return redirect('subject_list', company_id=company_id)
