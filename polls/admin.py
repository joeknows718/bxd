from django.contrib import admin
from polls.models import Poll, Choice

class ChoiceInline(admin.TabularInline): # adds poll choices as tabs
	model = Choice #adds model schema for choice
	extra = 3 

class PollAdmin(admin.ModelAdmin):#sets poll fields on backend
	fieldsets = [
		(None, {'fields':['question']}),#breaks into 2 field sets 1 for the question and another collapaseable one for poll info
		('Date information', {'fields':['pub_date'], 'classes':['collapse']})
		] 

	inlines = [ChoiceInline]# adds choice input fields as tabs
	list_display = ('question', 'pub_date', 'was_published_recently')# displays list of all questions, pub dates, and shows most recnt on main admin page
	list_filter = ['pub_date'] # be able to filet polls by pub date
	search_fields =['question'] #search polls by question
	date_hierarchy = 'pub_date' #rank by pub date

admin.site.register(Poll, PollAdmin)
