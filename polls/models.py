from django.db import models

class Poll(model.Models):
	question = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	def __unicode__(self):
		return self.question

class Choice(model.Models):
	poll = models.ForeignKey(Poll)
	choice_text = models.CharField(max_length=200)
	votes = models.IntergerField(default=0)
	def __unicode__(self):
		return self.choice_text
		
