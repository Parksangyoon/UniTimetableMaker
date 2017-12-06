from django.db import models
from djchoices import DjangoChoices, ChoiceItem


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

    name = models.CharField(max_length=100)
    num_of_people = models.IntegerField(null=True)
    classroom_type = models.IntegerField(choices=Type.choices)
