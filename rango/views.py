from django.http import HttpResponse 
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category
from rango.models import Page	

def index(request):
		#Request the context of the request
		#context contains info ei client machine detials
		context = RequestContext(request)
		#Const. A dict. to pass to template engine as context
		#bold message dict. key is the same as bold message embedded in index rango index.html
		category_list = Category.objects.order_by('likes')[:5] #create a list of top 5 categories fro the Catefory model, and ordering list by number of likes
		context_dict = {'categories' : category_list}#showing all categories listed and ordered to be placed in template 
		#return rendered response and send to client 
		#use shortcut funtion to simplify
		#the first parameter in this render respnse is the template that gets called
		for category in category_list :
			category.url = category.name.replace(' ', '_')
		return render_to_response('rango/index.html', context_dict, context)


def about(request):
	#return HttpResponse("<a href='/rango/'>BXD</a> Bronx Digital is a collaborative Community of Bronx based Coders")	
		context = RequestContext(request)
		context_dict = {}
		return render_to_response('rango/about.html', context_dict, context)

def category(request, category_name_url):#set a page request url map for category names
	context = RequestContext(request) #requests context from the request sent to us
	# change underscores in category name to spaces
	#urls don handle spaces well, so we will encode them with spaces again to get the name
	#then we can replace the underscores with spaces again to get the name. 
	category_name = category_name_url.replace('_', ' ')
	#create context dictionary which we can pass to template redering engine
	#we start by containing the name of the category passes by the user
	context_dict = {'category_name' : category_name}

	try:
		#can we find the category with the given name
		#if we cant the .get() method raises a DoesNotExist exception.
		#so the .get() method returnes one model instance or raises the exception\\\
		category = Category.objects.get(name=category_name)
		#retrieves all of the associated pages
		#filter returns >=1 model instance 
		pages = Page.objects.filter(category=category)
		#adds the page search results to the template context under the name pages
		context_dict['pages'] = pages
		#we also add the category object from db to context dict. 
		#and use this in the template to verify that the category exists. 
		context_dict['category'] = category
	except Category.DoesNotExist:
		#we get her if we can not find the category
		#we dont do anything - template displays no category message
		pass
	#got to render the resp.  and send to client
	return render_to_response('rango/category.html', context_dict, context)	

