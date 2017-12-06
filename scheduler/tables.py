import django_tables2 as tables

from scheduler.models.classroom_m import ClassroomInfo
from scheduler.string_name import CLASSROOM_NAME, NUM_OF_PEOPLE, CLASSROOM_TYPE


class ClassroomTable(tables.Table):

    class Meta:
        fields = [CLASSROOM_NAME, NUM_OF_PEOPLE, CLASSROOM_TYPE]
        model = ClassroomInfo
        template = 'django_tables2/bootstrap.html'
