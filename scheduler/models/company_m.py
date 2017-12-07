from django.db import models

from scheduler.string_name import NAME, FIELD, TERM, DATE


class CompanyInfo(models.Model):
    def get_model(self):
        return {
            NAME: self.name,
            FIELD: self.field_of,
            TERM: self.term,
            DATE: self.date,
        }

    def set_model(self, data):
        self.objects.count()
        CompanyInfo(name=data.get(NAME), field_of=data.get(FIELD), term=data.get(TERM), data=data.get(DATE)).save()

    name = models.CharField(max_length=100)
    field_of = models.CharField(max_length=100)
    term = models.IntegerField(null=True)
    date = models.DateTimeField(blank=True)
    sheet_name = models.CharField(max_length=100)
