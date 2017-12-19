from django.db import models
from djchoices import DjangoChoices, ChoiceItem

from scheduler.models.classroom_m import ClassroomInfo
from scheduler.models.company_m import CompanyInfo
from scheduler.string_name import NUM_OF_PEOPLE, MAJOR, GRADE, COMPLETION_TYPE, NAME, CREDIT, DURATION, \
    PROFESSOR, COMPANY, CLASSROOM, WEEK, RANGE_FROM, RANGE_TO, START_TIME, END_TIME, WEEK_NAME_KR, ID, SET_TIMETABLE


class SubjectInfo(models.Model):
    # Choices
    class CompletionType(DjangoChoices):
        MAJOR_ESSENTIAL = ChoiceItem(0)
        MAJOR_SELECT = ChoiceItem(1)

        @classmethod
        def to_string(cls, subject_type):
            if subject_type == 0:
                return '전필'
            elif subject_type == 1:
                return '전선'

        @classmethod
        def from_string(cls, string_of_type):
            if string_of_type == '전필':
                return SubjectInfo.CompletionType.MAJOR_ESSENTIAL
            elif string_of_type == '전선':
                return SubjectInfo.CompletionType.MAJOR_SELECT

    class WeekType(DjangoChoices):
        MON = ChoiceItem(0)
        TUES = ChoiceItem(1)
        WED = ChoiceItem(2)
        THURS = ChoiceItem(3)
        FRI = ChoiceItem(4)
        SAT = ChoiceItem(5)
        SUN = ChoiceItem(6)

        @classmethod
        def to_string(cls, subject_type):
            return WEEK_NAME_KR[subject_type]

        @classmethod
        def from_string(cls, string_of_type):
            return ChoiceItem(WEEK_NAME_KR.index(string_of_type))

    def get_model(self):
        return {
            ID: self.id,
            MAJOR: self.major,
            GRADE: self.grade,
            COMPLETION_TYPE: self.completion_type,
            NAME: self.name,
            CREDIT: self.credit,
            DURATION: self.duration,
            PROFESSOR: self.professor,
            NUM_OF_PEOPLE: self.num_of_people,
            COMPANY: self.company,
            CLASSROOM: self.classroom,
            WEEK: self.week,
            RANGE_FROM: self.range_from,
            RANGE_TO: self.range_to,
            START_TIME: self.start_time,
            END_TIME: self.end_time,
            SET_TIMETABLE: self.set_timetable,
        }

    def set_model(self, data):
        self.objects.count()
        if data.get(SET_TIMETABLE) is None:
            data[SET_TIMETABLE] = False
        set_data = SubjectInfo(
            major=data.get(MAJOR), grade=data.get(GRADE), completion_type=data.get(COMPLETION_TYPE),
            name=data.get(NAME), credit=data.get(CREDIT), duration=data.get(DURATION), company=data.get(COMPANY),
            num_of_people=data.get(NUM_OF_PEOPLE), professor=data.get(PROFESSOR), start_time=data.get(START_TIME),
            week=data.get(WEEK), end_time=data.get(END_TIME), range_from=data.get(RANGE_FROM),
            range_to=data.get(RANGE_TO), classroom=data.get(CLASSROOM), set_timetable=data.get(SET_TIMETABLE),
        )
        set_data.save()

    def update_model(self, data, company_id):
        if self.objects.count() != 0:
            try:
                update_data = SubjectInfo.objects.filter(company_id=company_id).filter(row_num=data.get(ID))
                update_data.major = data.get(MAJOR)
                update_data.grade = data.get(GRADE)
                update_data.completion_type = data.get(COMPLETION_TYPE)
                update_data.name = data.get(NAME)
                update_data.credit = data.get(CREDIT)
                update_data.duration = data.get(DURATION)
                update_data.num_of_people = data.get(NUM_OF_PEOPLE)
                update_data.professor = data.get(PROFESSOR)
                update_data.company = data.get(COMPANY)
                update_data.start_time = data.get(START_TIME)
                update_data.end_time = data.get(END_TIME)
                update_data.week = data.get(WEEK)
                update_data.range_from = data.get(RANGE_FROM)
                update_data.range_to = data.get(RANGE_TO)
                update_data.classroom = data.get(CLASSROOM)
                update_data.set_timetable = data.get(SET_TIMETABLE)
                update_data.save()
            except SubjectInfo.DoesNotExist:
                print("SubjectInfo does not exist")

    major = models.CharField(null=True, max_length=100)                                  # 전공
    grade = models.IntegerField(null=True)                                               # 학년
    completion_type = models.IntegerField(choices=CompletionType.choices)                # 이수구분
    name = models.CharField(null=True, max_length=100)                                   # 교과목명
    credit = models.IntegerField(null=True)                                              # 학점
    duration = models.IntegerField(null=True)                                            # 총 강의시간
    professor = models.CharField(null=True, max_length=100)                              # 교수님
    num_of_people = models.IntegerField(null=True)                                       # 수강인원
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE)                   # 회사
    range_from = models.IntegerField(null=True)                                          # 시간표 범위(시작)
    range_to = models.IntegerField(null=True)                                            # 시간표 범위(끝)
    classroom = models.ForeignKey(ClassroomInfo, null=True, on_delete=models.SET_NULL)   # 강의실
    week = models.IntegerField(choices=WeekType.choices, null=True)                      # 요일
    start_time = models.IntegerField(null=True)                                          # 시작시간
    end_time = models.IntegerField(null=True)                                            # 끝 시간
    set_timetable = models.BooleanField(default=False)                                   # 시간표 설정 여부
