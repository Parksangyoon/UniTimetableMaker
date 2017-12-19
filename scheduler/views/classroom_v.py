import gspread
from django.shortcuts import redirect
from django.views.generic import ListView

from scheduler.db_manager import set_db_data
from scheduler.google_sheet import read_sheet
from scheduler.models.classroom_m import ClassroomInfo
from scheduler.models.company_m import CompanyInfo
from scheduler.string_name import CLASSROOM_TYPE, CLASSROOM_KEY_NAME, SHEET_CLASSROOM, COMPANY, SCHEDULE, RANGE_FROM, \
    RANGE_TO
from scheduler.util import list_to_str
from ..tables import ClassroomTable
from ..views.common_v import request_table_config


class ClassroomListView(ListView):
    template_name = 'timetable/classroom_t.html'
    model = ClassroomInfo
    object_list = None

    def get_queryset(self):
        classroom_list = ClassroomInfo.objects.filter(company_id=self.kwargs['company_id'])
        return classroom_list

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)
        table = ClassroomTable(self.object_list)
        request_table_config(request, table)
        context['table'] = table
        context['company_name'] = CompanyInfo.objects.get(id=self.kwargs['company_id']).name
        return self.render_to_response(context)


def update_classroom(request, company_id):
    classroom_list = ClassroomInfo.objects.all()
    for classroom in classroom_list:
        classroom.delete()
    get_classroom_list(company_id)
    return redirect('classroom_list', company_id=company_id)


# 시트에서 강의실 데이터 가져오기
def get_classroom_list(company_id):
    company_data = CompanyInfo.objects.get(id=company_id)
    try:
        sheet = read_sheet(company_data.sheet_name, "강의실")
    except gspread.exceptions.SpreadsheetNotFound:
        return redirect('home')
    classrooms_of_sheet = sheet.get_all_records(head=1)
    classroom_list = []
    classroom = dict()
    for dict_data in classrooms_of_sheet:
        for data in dict_data.keys():
            if '종류' in data:
                classroom[CLASSROOM_TYPE] = ClassroomInfo.Type.from_string(dict_data.get(data))
            else:
                classroom[CLASSROOM_KEY_NAME[SHEET_CLASSROOM.index(data)]] = dict_data.get(data)
        classroom[COMPANY] = company_data
        schedule_list = [[] for i in range(7)]
        classroom[SCHEDULE] = list_to_str(schedule_list)
        classroom_list.append(classroom)
        classroom = dict()
    set_db_data(ClassroomInfo, classroom_list)
    return redirect('classroom_list', company_id=company_id)


def set_classroom(request, company_id):
    if request.method == 'POST':
        selected_subject_list = request.POST.getlist('select_classroom')
        range_from = request.POST.get(RANGE_FROM)
        range_to = request.POST.get(RANGE_TO)
        select_all = request.POST.get("select_all")

        if range_from is '':
            range_from = 9
        if range_to is '':
            range_to = 18

        if select_all is not None:
            classroom_list = ClassroomInfo.objects.filter(company_id=company_id)
            for classroom in classroom_list:
                classroom.range_from = range_from
                classroom.range_to = range_to
                classroom.save()
        else:
            for classroom_id in selected_subject_list:
                classroom = ClassroomInfo.objects.get(id=classroom_id)
                classroom.range_from = range_from
                classroom.range_to = range_to
                classroom.save()

    return redirect('classroom_list', company_id=company_id)
