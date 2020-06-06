from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns


# Create your models here.
class DataMgtOptions(models.Model):
#	name = models.CharField(max_length=200)
	opt1 = models.BooleanField()
	opt2 = models.BooleanField()
	opt3 = models.BooleanField()
	opt4 = models.BooleanField()
	opt5 = models.BooleanField()
	opt6 = models.BooleanField()
	opt7 = models.BooleanField()
	opt8 = models.BooleanField()
	opt9 = models.BooleanField()
	opt10 = models.BooleanField()
	opt11 = models.BooleanField()

	# def __str__(self):
	# 	return self.name

