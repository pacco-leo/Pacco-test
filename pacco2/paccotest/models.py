from django.db import models

# Create your models here.


#An Answer to a Question
class Answer(models.Model):
    answer_text = models.CharField(max_length=200)

    def __unicode__(self):
        return self.answer_text


#An answer to a Question
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    order_index = models.IntegerField()
    answers = models.ManyToManyField(Answer)  #Many-to-many relationship

    def __unicode__(self):
        return self.question_text

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

class Probe(models.Model):
    name = models.CharField(max_length=200)
    channel = models.IntegerField()
    order = models.IntegerField()

    def __unicode__(self):
        return self.name + " , " + str(self.channel)

#A ProbeType
# class ProbeType(models.Model):
#     PH = 'REDOX'
#     REDOX = 'REDOX'
#     CONDUCTIVITY = 'CONDUCTIVITY'
#     DO = 'DO'
#     TEMPERATURE = 'TEMPERATURE'

#A ProbeMeasure
class ProbeMeasure(models.Model):
    survey = models.ForeignKey(Survey)
    probeType = models.ForeignKey(Probe)
    measure = models.FloatField('measure')

    def __unicode__(self):
        return self.survey + " , " + self.probeType + " , " + self.measure





