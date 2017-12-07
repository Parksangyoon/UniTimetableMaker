from django.db import models
from djchoices import DjangoChoices, ChoiceItem

from scheduler.string_name import NAME, NUM_OF_PEOPLE, CLASSROOM_TYPE


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
            if string_of_classroom == '일반':
                return ClassroomInfo.Type.NORMAL
            elif string_of_classroom == '실습':
                return ClassroomInfo.Type.PRACTICE

    def get_model(self):
        return {
            NAME: self.name,
            CLASSROOM_TYPE: self.classroom_type,
            NUM_OF_PEOPLE: self.num_of_people,
        }

    def set_model(self, classroom_data):
        self.objects.count()
        set_data = ClassroomInfo(
            name=classroom_data.get(NAME), num_of_people=classroom_data.get(NUM_OF_PEOPLE),
            classroom_type=classroom_data.get(CLASSROOM_TYPE)
        )
        set_data.save()

    name = models.CharField(max_length=100)
    num_of_people = models.IntegerField(null=True)
    classroom_type = models.IntegerField(choices=Type.choices)
