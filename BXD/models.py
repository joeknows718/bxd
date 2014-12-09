from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=128, unique=True) #if unique is set to true this only on instace of field can exist throught db model
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	slug = models.SlugField(unique=True)
	
	class Meta:
		verbose_name_plural = 'Categories'

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name	

class Page(models.Model):
	category = models.ForeignKey(Category) #forgienkey creates a one to many relationship _> 1 Categorty many Pages OnetoOne is 121 and ManytoMany ect
	title = models.CharField(max_length=128) #stores metadata page title
	url = models.URLField()					#stores URLs
	views = models.IntegerField(default=0) #stores int also DateFeilds store dates

	def __unicode__(self):
		return self.title

class Project(models.Model):
	creator = models.ForeignKey(User)
	project_name = models.CharField(max_length=128)
	website = models.URLField(blank=True)
	github = models.URLField(blank=True)
	description = models.CharField(max_length=255, unique=True)
	likes = models.IntegerField(default=0)
	slug = models.SlugField(unique=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.project_name)
		super(Project, self).save(*args, **kwargs)
	
	def __unicode__(self):

		return self.project_name

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)

	def __unicode__(self):
		return self.user.username

