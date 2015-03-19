from django.db import models

# Create your models here.

class PlateformInfo(models.Model):
    software_version = models.FloatField()
    rpi_id = models.IntegerField()

    def __unicode__(self):
        return "Software version : "+ str(self.software_version) + " --- RaspberryID : " + str(self.rpi_id)

#An Answer to a Question
class Answer(models.Model):
    text = models.CharField(max_length=200)
    order = models.IntegerField()

    def __unicode__(self):
        return self.text


#An answer to a Question
class Question(models.Model):
    text = models.CharField('text',max_length=300)
    order = models.IntegerField()
    actif = models.BooleanField(default=True)
    answers = models.ManyToManyField(Answer)  #Many-to-many relationship

    def __unicode__(self):
        return self.text

    class Meta:
        #pass
        ordering = ['order']


class Probe(models.Model):
    name = models.CharField(max_length=200)
    text = models.CharField('text',max_length=200)
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

# -------------- User Values Related Classes --------------
#A Survey
class Survey(models.Model):
    latitude = models.FloatField('latitude')
    longitude = models.FloatField('longitude')
    elevation = models.FloatField('elevation')
    utc = models.DateTimeField('date')
    uploadedToServer = models.BooleanField('uploadedToServer', default=False)

    def __unicode__(self):
        return str(self.latitude) + " , " + str(self.longitude) + " , " + str(self.elevation) + " , " + str(self.utc)

#An UserAnswer to a Question
class UserAnswer(models.Model):
    survey = models.ForeignKey(Survey)
    answer = models.ForeignKey(Answer)
    question = models.ForeignKey(Question)

    def __unicode__(self):
        return "Survey :" + str(self.survey.id) + " - Answer: " + str(self.answer.id) + " to question: " + str(self.question.id)


#A ProbeMeasure
class ProbeMeasure(models.Model):
    survey = models.ForeignKey(Survey)
    probeType = models.ForeignKey(Probe)
    measure = models.CharField('measure',max_length=200)

    def __unicode__(self):
        return "Survey : " + str(self.survey.id) + " - " + str(self.probeType.name) + " : " + str(self.measure)
# -------------- /User Values Related Classes --------------





