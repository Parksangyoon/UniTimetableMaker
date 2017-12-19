import gspread
from django.shortcuts import redirect
from django.views.generic import ListView

from scheduler.db_manager import set_db_data
from scheduler.google_sheet import read_sheet
from scheduler.models.classroom_m import ClassroomInfo
from scheduler.models.company_m import CompanyInfo
from scheduler.models.subject_m import SubjectInfo
from scheduler.string_name import COMPLETION_TYPE, SUBJECT_KEY_NAME, SHEET_SUBJECT, COMPANY, WEEK_NAME_KR
from ..tables import SubjectTable
from ..views.common_v import request_table_config


class SubjectListView(ListView):
    template_name = 'timetable/subject_t.html'
    model = SubjectInfo
    object_list = None

    def get_queryset(self):
        subject_list = SubjectInfo.objects.filter(company_id=self.kwargs['company_id'])
        return subject_list

    def get(self, request, *args, **kwargs):

        self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)
        table = SubjectTable(self.object_list)
        request_table_config(request, table)
        context['table'] = table
        context['company_name'] = CompanyInfo.objects.get(id=self.kwargs['company_id']).name
        context['classroom_list'] = ClassroomInfo.objects.filter(company_id=self.kwargs['company_id'])
        context['week_list'] = WEEK_NAME_KR
        return self.render_to_response(context)


def update_subject(request, company_id):
    classroom_list = ClassroomInfo.objects.filter(company_id=company_id)

    if classroom_list.__sizeof__() is not 0:
        schedule_list = [[] for i in range(7)]
        for classroom in classroom_list:
            classroom.schedule = schedule_list
            classroom.save()

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
                subject[COMPLETION_TYPE] = SubjectInfo.CompletionType.from_string(dict_data[data])
            else:
                subject[SUBJECT_KEY_NAME[SHEET_SUBJECT.index(data)]] = dict_data[data]
                subject[COMPANY] = company_data
        subject_list.append(subject)
        subject = dict()
    set_db_data(SubjectInfo, subject_list)
    return redirect('subject_list', company_id=company_id)


# advertisement 의 content 선택
def set_subject(request, company_id):

    if request.method == 'POST':
        selected_subject_list = request.POST.getlist('select_subject')
        select_from = request.POST.get('select_from')
        select_to = request.POST.get('select_to')
        classroom_id = request.POST.get('classroom_id')
        week = request.POST.get('week')
        select_all = request.POST.get('select_all')

        if select_from is '':
            select_from = 9
        if select_to is '':
            select_to = 0
            data_list = SubjectInfo.objects.filter(company_id=company_id)
            for i in data_list:
                select_to = select_to + i.duration
            select_to = 19

        if select_all is not None:
            subject_list = SubjectInfo.objects.filter(company_id=company_id)
            for subject in subject_list:
                subject.range_from = select_from
                subject.range_to = select_to
                if classroom_id not in "None":
                    subject.classroom_id = classroom_id
                if week not in "None":
                    subject.week = week
                subject.set_timetable = False
                subject.save()
        else:
            for subject_id in selected_subject_list:
                subject = SubjectInfo.objects.filter(company_id=company_id).get(id=subject_id)
                subject.range_from = select_from
                subject.range_to = select_to
                if classroom_id not in "None":
                    subject.classroom_id = classroom_id
                if week not in "None":
                    subject.week = week
                subject.set_timetable = False
                subject.save()

    return redirect('subject_list', company_id=company_id)
