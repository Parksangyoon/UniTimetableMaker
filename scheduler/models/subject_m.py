from django.db import models
from djchoices import DjangoChoices, ChoiceItem

from scheduler.string_name import NUM_OF_PEOPLE, MAJOR, GRADE, COMPLETION_TYPE, NAME, CREDIT, DURATION, \
    DURATION_OF_THEORY, DURATION_OF_PRACTICE, PROFESSOR


class SubjectInfo(models.Model):
    # Choices
    class Type(DjangoChoices):
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
                return SubjectInfo.Type.MAJOR_ESSENTIAL
            elif string_of_type == '전선':
                return SubjectInfo.Type.MAJOR_SELECT

    def get_model(self):
        return {
            MAJOR: self.major,
            GRADE: self.grade,
            COMPLETION_TYPE: self.completion_type,
            NAME: self.name,
            CREDIT: self.credit,
            DURATION: self.duration,
            DURATION_OF_THEORY: self.duration_of_theory,
            DURATION_OF_PRACTICE: self.duration_of_practice,
            PROFESSOR: self.professor,
            NUM_OF_PEOPLE: self.num_of_people,
        }

    def set_model(self, data):
        self.objects.count()
        set_data = SubjectInfo(
            major=data.get(MAJOR), grade=data.get(GRADE), completion_type=data.get(COMPLETION_TYPE),
            name=data.get(NAME), credit=data.get(CREDIT), duration=data.get(DURATION),
            duration_of_theory=data.get(DURATION_OF_THEORY), num_of_people=data.get(NUM_OF_PEOPLE),
            duration_of_practice=data.get(DURATION_OF_PRACTICE), professor=data.get(PROFESSOR)
        )
        set_data.save()

    major = models.CharField(null=True, max_length=100)             # 전공
    grade = models.IntegerField(null=True)                          # 학년
    completion_type = models.IntegerField(choices=Type.choices)     # 이수구분
    name = models.CharField(null=True, max_length=100)              # 교과목명
    credit = models.IntegerField(null=True)                         # 학점
    duration = models.IntegerField(null=True)                       # 총 강의시간
    duration_of_theory = models.IntegerField(null=True)             # 이론 시간
    duration_of_practice = models.IntegerField(null=True)           # 실습 시간
    professor = models.CharField(null=True, max_length=100)         # 교수님
    num_of_people = models.IntegerField(null=True)                  # 수강인원
