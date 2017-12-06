from django.views.generic import ListView

from scheduler.models.subject_m import SubjectInfo
from ..tables import SubjectTable
from ..views.common_v import request_table_config


class SubjectListView(ListView):
    template_name = 'subject_t.html'
    model = SubjectInfo
    object_list = None

    def get_queryset(self):
        subject_list = SubjectInfo.objects.all()
        return subject_list

    def get(self, request, *args, **kwargs):

        self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)
        table = SubjectTable(self.object_list)
        request_table_config(request, table)
        context['table'] = table
        return self.render_to_response(context)
