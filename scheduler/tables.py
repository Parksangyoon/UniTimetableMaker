import django_tables2 as tables

from scheduler.models.classroom_m import ClassroomInfo
from scheduler.models.subject_m import SubjectInfo
from scheduler.string_name import NAME, NUM_OF_PEOPLE, CLASSROOM_TYPE, MAJOR, GRADE, COMPLETION_TYPE,\
    CREDIT, DURATION, DURATION_OF_THEORY, DURATION_OF_PRACTICE, PROFESSOR


class ClassroomTable(tables.Table):
    name = tables.Column(verbose_name="강의실", accessor=NAME)
    num_of_people = tables.Column(verbose_name="수용 인원", accessor=NUM_OF_PEOPLE)
    classroom_type = tables.Column(verbose_name="종류", accessor=CLASSROOM_TYPE)

    def __init__(self, *args, **kwargs):
        super(ClassroomTable, self).__init__(*args, **kwargs)

    class Meta:
        fields = []
        model = ClassroomInfo
        template = 'django_tables2/bootstrap.html'


class SubjectTable(tables.Table):
    major = tables.Column(verbose_name="전공", accessor=MAJOR)
    grade = tables.Column(verbose_name="학년", accessor=GRADE)
    completion_type = tables.Column(verbose_name="이수 구분", accessor=COMPLETION_TYPE)
    name = tables.Column(verbose_name="교과목명", accessor=NAME)
    credit = tables.Column(verbose_name="학점", accessor=CREDIT)
    duration = tables.Column(verbose_name="총 강의시간", accessor=DURATION)
    duration_of_theory = tables.Column(verbose_name="이론 시간", accessor=DURATION_OF_THEORY)
    duration_of_practice = tables.Column(verbose_name="실습 시간", accessor=DURATION_OF_PRACTICE)
    professor = tables.Column(verbose_name="교수님", accessor=PROFESSOR)
    num_of_people = tables.Column(verbose_name="수강 인원", accessor=NUM_OF_PEOPLE)

    def __init__(self, *args, **kwargs):
        super(SubjectTable, self).__init__(*args, **kwargs)

    class Meta:
        fields = []
        model = SubjectInfo
        template = 'django_tables2/bootstrap.html'
