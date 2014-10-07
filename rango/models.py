from django.db import models
from datetime import datetime 

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=128, unique=True) #if unique is set to true this only on instace of field can exist throught db model
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	class Meta:
		verbose_name_plural = 'Categories'
	def __unicode__(self):
		return self.name	

class Page(models.Model):
	category = models.ForeignKey(Category) #forgienkey creates a one to many relationship _> 1 Categorty many Pages OnetoOne is 121 and ManytoMany ect
	title = models.CharField(max_length=128) #stores metadata page title
	url = models.URLField()					#stores URLs
	views = models.IntegerField(default=0) #stores int also DateFeilds store dates

	def __unicode__(self):
		return self.title

class Event(models.Model):
	category = models.ForeignKey(Category)
	name = models.CharField(max_length=128, unique=True)
	RSVP = models.URLField()	
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()

	def __unicode__(self):
		return self.name 
