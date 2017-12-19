from django.db import models
from djchoices import DjangoChoices, ChoiceItem

from scheduler.models.company_m import CompanyInfo
from scheduler.string_name import NAME, NUM_OF_PEOPLE, CLASSROOM_TYPE, COMPANY, SCHEDULE, RANGE_FROM, RANGE_TO


class ClassroomInfo(models.Model):
    # Choices
    class Type(DjangoChoices):
        NORMAL = ChoiceItem(0)
        PRACTICE = ChoiceItem(1)

        @classmethod
        def to_string(cls, classroom_type):
            if classroom_type == 0:
                return '일반'
            elif classroom_type == 1:
                return '실습'

        @classmethod
        def from_string(cls, string_of_classroom):
            if '일반' in string_of_classroom:
                return ClassroomInfo.Type.NORMAL
            elif '실습' in string_of_classroom:
                return ClassroomInfo.Type.PRACTICE

    def get_model(self):
        return {
            NAME: self.name,
            CLASSROOM_TYPE: self.classroom_type,
            NUM_OF_PEOPLE: self.num_of_people,
            COMPANY: self.company_id,
            SCHEDULE: self.schedule,
            RANGE_FROM: self.range_from,
            RANGE_TO: self.range_to,
        }

    def set_model(self, data):
        self.objects.count()
        set_data = ClassroomInfo(
            name=data.get(NAME), num_of_people=data.get(NUM_OF_PEOPLE), company=data.get(COMPANY),
            schedule=data.get(SCHEDULE), classroom_type=data.get(CLASSROOM_TYPE), range_from=data.get(RANGE_FROM),
            range_to=data.get(RANGE_TO),
        )
        set_data.save()

    name = models.CharField(max_length=100)
    num_of_people = models.IntegerField(null=True)
    classroom_type = models.IntegerField(choices=Type.choices)
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE)
    range_from = models.IntegerField(null=True)
    range_to = models.IntegerField(null=True)
    schedule = models.CharField(null=True, max_length=100)
