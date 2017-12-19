import django_tables2 as tables
from django_tables2.utils import A

from scheduler.models.classroom_m import ClassroomInfo
from scheduler.models.company_m import CompanyInfo
from scheduler.models.subject_m import SubjectInfo
from scheduler.string_name import NAME, NUM_OF_PEOPLE, CLASSROOM_TYPE, MAJOR, GRADE, COMPLETION_TYPE, \
    CREDIT, DURATION, PROFESSOR, FIELD, TERM, DATE, RANGE_FROM, \
    RANGE_TO


class ClassroomTable(tables.Table):
    name = tables.Column(verbose_name="강의실", accessor=NAME)
    num_of_people = tables.Column(verbose_name="수용 인원", accessor=NUM_OF_PEOPLE)
    classroom_type = tables.Column(verbose_name="종류", accessor=CLASSROOM_TYPE)
    range_from = tables.Column(verbose_name="Open", accessor=RANGE_FROM)
    range_to = tables.Column(verbose_name="Close", accessor=RANGE_TO)
    select_classroom = tables.CheckBoxColumn(accessor="pk", orderable=False)

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
    professor = tables.Column(verbose_name="교수님", accessor=PROFESSOR)
    num_of_people = tables.Column(verbose_name="수강 인원", accessor=NUM_OF_PEOPLE)
    range_from = tables.Column(verbose_name="from", accessor="range_from")
    range_to = tables.Column(verbose_name="to", accessor="range_to")
    classroom = tables.Column(verbose_name="강의실", accessor="classroom.name")
    week = tables.Column(verbose_name="요일", accessor="week")
    select_subject = tables.CheckBoxColumn(accessor="pk", orderable=False)

    def __init__(self, *args, **kwargs):
        super(SubjectTable, self).__init__(*args, **kwargs)

    class Meta:
        fields = []
        model = SubjectInfo
        template = 'django_tables2/bootstrap.html'


class CompanyTable(tables.Table):
    id = tables.LinkColumn(viewname='edit_company', args=[A('pk')], verbose_name="편집")
    name = tables.LinkColumn(viewname='classroom_list', args=[A('id')], verbose_name="학교", accessor=NAME)
    field_of = tables.Column(verbose_name="전공", accessor=FIELD)
    term = tables.Column(verbose_name="학기", accessor=TERM)
    date = tables.DateTimeColumn(verbose_name="날짜", format="Y-m-d H:i")
    sheet_name = tables.Column(verbose_name="google sheet name", accessor="sheet_name")

    def __init__(self, *args, **kwargs):
        super(CompanyTable, self).__init__(*args, **kwargs)

    class Meta:
        model = CompanyInfo
        fields = ["id", NAME, FIELD, TERM, DATE, "sheet_name"]
        template = 'django_tables2/bootstrap.html'


class TimetableTable(tables.Table):
    major = tables.Column(verbose_name="전공", accessor=MAJOR)
    grade = tables.Column(verbose_name="학년", accessor=GRADE)
    completion_type = tables.Column(verbose_name="이수 구분", accessor=COMPLETION_TYPE)
    name = tables.Column(verbose_name="교과목명", accessor=NAME)
    duration = tables.Column(verbose_name="총 강의시간", accessor=DURATION)
    classroom = tables.Column(verbose_name="강의실", accessor="classroom.name")
    week = tables.Column(verbose_name="요일", accessor="week")
    start_time = tables.Column(verbose_name="Start Time", accessor="start_time")
    end_time = tables.Column(verbose_name="End Time", accessor="end_time")
    select_subject = tables.CheckBoxColumn(accessor="pk", orderable=False)

    def __init__(self, *args, **kwargs):
        super(TimetableTable, self).__init__(*args, **kwargs)

    class Meta:
        fields = []
        model = SubjectInfo
        template = 'django_tables2/bootstrap.html'
