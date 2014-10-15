from django.db import models

# Create your models here.
class Reponses(models.Model):

	titre = models.CharField(max_length=2)
	datetime = models.CharField(max_length=25,null=True)
	gps1 = models.CharField(max_length=20,null=True)
	gps2 = models.CharField(max_length=20,null=True)
	gps3 = models.CharField(max_length=20,null=True)
	q1 = models.IntegerField(max_length=1,null=True)
	q2 = models.IntegerField(max_length=1,null=True)
	q3 = models.IntegerField(max_length=1,null=True)
	q4 = models.IntegerField(max_length=1,null=True)
	q5 = models.IntegerField(max_length=1,null=True)
	q6 = models.IntegerField(max_length=1,null=True)
	q7 = models.IntegerField(max_length=1,null=True)
	q8 = models.IntegerField(max_length=1,null=True)
	q9 = models.IntegerField(max_length=1,null=True)
	q10 = models.IntegerField(max_length=1,null=True)
	q11 = models.IntegerField(max_length=1,null=True)
	q12 = models.IntegerField(max_length=1,null=True)
	s1 = models.CharField(max_length=50,null=True)
	s2 = models.CharField(max_length=50,null=True)
	s3 = models.CharField(max_length=50,null=True)
	s4 = models.CharField(max_length=50,null=True)
	s5 = models.CharField(max_length=50,null=True)
	
	def get_fields(self):
		return[(field.name, field.value_to_string(self)) for field in Reponses._meta.fields]

	def __unicode__(self):
		return self.titre

