from django.http import HttpResponse 
from django.template import RequestContext
from dango.shortcuts import render_to_response

def index(request):
		#Request the context of the request
		#context contains info ei client machine detials
		context = RequestContext(request)
		#Const. A dict. to pass to template engine as context
		#bold message dict. key is the same as bold message embedded in index rango index.html
		context_dict = {'boldmessage' : "I am bold font from the context"}

		#return rendered response and send to client 
		#use shortcut funtion to simplify
		#the first parameter in this render respnse is the template that gets called
		retun render_to_response('rango/index.html', context_dict, context)


def about(request):
	return HttpResponse("<a href='/rango/'>BXD</a> Bronx Digital is a collaborative Community of Bronx based Coders")	
