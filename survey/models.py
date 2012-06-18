import datetime
from django.db import models

class Survey(models.Model):
    title = models.CharField(max_length=60)
    opens = models.DateField()
    closes = models.DateField()

    def save(self, **kwargs):
        if not self.pk and self.opens and not self.closes:
            #self.closes = self.opens + datetime.timedelta(7)
            self.closes = self.opens
        super(Survey, self).save(**kwargs)

class Question(models.Model):
    question = models.CharField(max_length=200)
    survey = models.ForeignKey(Survey)

class Answer(models.Model):
    answer = models.CharField(max_length=200)
    question = models.ForeignKey(Question)
    votes = models.IntegerField(default=0)
