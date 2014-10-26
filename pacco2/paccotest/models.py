from django.db import models

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    order_index = models.IntegerField()

    def __unicode__(self):
        return self.question_text

    class Meta:
        pass
        #ordering = ('order_index')

class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer_text = models.CharField(max_length=200)

    def __unicode__(self):
        return self.answer_text

    class Meta:
        pass
        #ordering = ('order_index')

#A Survey
class Survey(models.Model):
    latitude = models.FloatField('latitude')
    longitude = models.FloatField('longitude')
    elevation = models.FloatField('elevation')
    utc = models.DateTimeField('date')

    def __unicode__(self):
        return self.latitude + " , " + self.longitude + " , " + self.elevation + " , " + self.utc

#An UserAnswer to a Question
class UserAnswer(models.Model):
    survey = models.ForeignKey(Survey)
    answer = models.ForeignKey(Answer)

#A ProbeType
class ProbeType(models.Model):
    PH = 'REDOX'
    REDOX = 'REDOX'
    CONDUCTIVITY = 'CONDUCTIVITY'
    DO = 'DO'
    TEMPERATURE = 'TEMPERATURE'

#A ProbeMeasure
class ProbeMeasure(models.Model):
    survey = models.ForeignKey(Survey)
    probeType = models.ForeignKey(ProbeType)
    mesure = models.FloatField('measure')


