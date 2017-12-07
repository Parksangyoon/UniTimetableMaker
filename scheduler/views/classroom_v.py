from django.shortcuts import redirect
from django.views.generic import ListView

from scheduler.db_manager import set_db_data
from scheduler.google_sheet import read_sheet
from scheduler.models.classroom_m import ClassroomInfo
from scheduler.string_name import CLASSROOM_TYPE, CLASSROOM_KEY_NAME, SHEET_CLASSROOM
from ..tables import ClassroomTable
from ..views.common_v import request_table_config


class ClassroomListView(ListView):
    template_name = 'classroom_t.html'
    model = ClassroomInfo
    object_list = None

    def get_queryset(self):
        classroom_list = ClassroomInfo.objects.all()
        if classroom_list.__len__() is 0:
            get_classroom_list()
        return classroom_list

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)
        table = ClassroomTable(self.object_list)
        request_table_config(request, table)
        context['table'] = table
        return self.render_to_response(context)


def update_classroom(request):
    classroom_list = ClassroomInfo.objects.all()
    for classroom in classroom_list:
        classroom.delete()
    get_classroom_list()
    return redirect('classroom_list')


# 시트에서 강의실 데이터 가져오기
def get_classroom_list():
    sheet = read_sheet("시간표", "강의실")
    classrooms_of_sheet = sheet.get_all_records(head=1)
    classroom_list = []
    classroom = dict()
    classroom.keys()
    for dict_data in classrooms_of_sheet:
        for data in dict_data.keys():
            if '종류' in data:
                classroom[CLASSROOM_TYPE] = ClassroomInfo.Type.from_string(dict_data[data])
            else:
                classroom[CLASSROOM_KEY_NAME[SHEET_CLASSROOM.index(data)]] = dict_data[data]
        classroom_list.append(classroom)
        classroom = dict()
    set_db_data(ClassroomInfo, classroom_list)
