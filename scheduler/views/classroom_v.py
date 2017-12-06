from django.views.generic import ListView

from scheduler.models.classroom_m import ClassroomInfo
from ..tables import ClassroomTable
from ..views.common_v import request_table_config


class ClassroomListView(ListView):
    template_name = 'classroom_t.html'
    model = ClassroomInfo
    object_list = None

    def get_queryset(self):
        classroom_list = ClassroomInfo.objects.all()
        return classroom_list

    def get(self, request, *args, **kwargs):

        self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)
        table = ClassroomTable(self.object_list)
        request_table_config(request, table)
        context['table'] = table
        return self.render_to_response(context)
