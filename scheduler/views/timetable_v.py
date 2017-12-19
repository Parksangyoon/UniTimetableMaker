from django.shortcuts import redirect
from django.views.generic import ListView

from scheduler.models.company_m import CompanyInfo
from scheduler.models.subject_m import SubjectInfo
from scheduler.solver.function_of_timetable import assign_to_different_time
from scheduler.string_name import BEFORE_SUBJECT, AFTER_SUBJECT, ID, START_TIME, END_TIME
from ..tables import TimetableTable, SubjectTable
from ..views.common_v import request_table_config


class TimetableListView(ListView):
    template_name = 'timetable/timetable_t.html'
    model = SubjectInfo
    object_list = None

    def get_queryset(self):
        before_subject = []
        after_subject = []
        for subject in SubjectInfo.objects.filter(company_id=self.kwargs['company_id']):
            if subject.set_timetable:
                after_subject.append(subject)
            else:
                before_subject.append(subject)
        return {BEFORE_SUBJECT: before_subject, AFTER_SUBJECT: after_subject}

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)

        before_table = SubjectTable(self.object_list.get(BEFORE_SUBJECT))
        request_table_config(request, before_table)

        after_table = TimetableTable(self.object_list.get(AFTER_SUBJECT))
        request_table_config(request, after_table)

        context['before_table'] = before_table
        context['after_table'] = after_table
        context['company_name'] = CompanyInfo.objects.get(id=self.kwargs['company_id']).name
        return self.render_to_response(context)


def update_timetable(request, company_id):
    selected_subject_list = []
    if request.method == 'POST':
        selected_subject_list = request.POST.getlist('select_subject')
        timetable_type = request.POST.get('timetable_type')
        select_all = request.POST.get('select_all')

        group_by_week = [[] for i in range(8)]

        if select_all is not None:
            subject_list = SubjectInfo.objects.filter(company_id=company_id)
            for subject in subject_list:
                subject.set_timetable = True
                subject.save()
                if subject.week is None:
                    group_by_week[7].append(subject.get_model())
                else:
                    group_by_week[subject.week].append(subject.get_model())
        else:
            for index in selected_subject_list:
                subject = SubjectInfo.objects.get(id=index)
                subject.set_timetable = True
                subject.save()
                if subject.week is None:
                    group_by_week[7].append(subject.get_model())
                else:
                    group_by_week[subject.week].append(subject.get_model())

        for week_index, timetable in enumerate(group_by_week):
            assign_to_different_time(timetable, week_index)
            for data in timetable:
                subject = SubjectInfo.objects.get(id=data.get(ID))
                subject.start_time = data.get(START_TIME)
                subject.end_time = data.get(END_TIME)
                subject.save()

    return redirect('timetable', company_id=company_id)
