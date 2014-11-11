from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category, Project
from rango.models import Page	
from rango.forms import CategoryForm
from rango.forms import PageForm, UserForm, UserProfileForm, ProjectForm
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

def encodeUrl(str):
	return str.replace(' ','_')

def decodeUrl(str):
	return str.replace('_', ' ')
	

def index(request):
		#Request the context of the request
		#context contains info ei client machine detials
		request.session.set_test_cookie
		context = RequestContext(request)
		
		#Const. A dict. to pass to template engine as context
		#bold message dict. key is the same as bold message embedded in index BXD index.html
		category_list = Category.objects.order_by('likes')[:5] 
		page_list = Page.objects.order_by('views')[:5]#create a list of top 5 categories fro the Catefory model, and ordering list by number of likes
		context_dict = {'categories' : category_list, 'pages': page_list}#showing all categories listed and ordered to be placed in template 
		#return rendered response and send to client 
		#use shortcut funtion to simplify
		#the first parameter in this render respnse is the template that gets called
		for category in category_list :
			category.url = encodeUrl(category.name)

		if request.session.get('last_visit'):
			last_visit_time = request.session.get('last_visit')
			visits = request.session.get('visits', '0')

			if datetime.now - datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S").seconds > 10:
				request.session['visits'] = visits + 1 
				request.session['last_visit'] = str(datetime.now())

			else:
				request.session['last_visit'] = str(datetime.now())
				request.session['visits'] = 1  


		return render_to_response('rango/index.html', context_dict, context)
		

def resources(request):
		context = RequestContext(request)
		category_list = Category.objects.order_by('likes')[:10]
		page_list = Page.objects.order_by('views')[:20]
		context_dict = {'categories' : category_list, 'pages': page_list}
		for category in category_list :
			category.url = encodeUrl(category.name)
		return render_to_response('rango/resources.html', context_dict, context)



def about(request):
	#return HttpResponse("<a href='/BronxDigital/'>BXD</a> Bronx Digital is a collaborative Community of Bronx based Coders")	
		context = RequestContext(request)
		if request.session.get('visits'):
			count = request.session.get('visits')
		else:
			count = 0
		context_dict = { 'visits' : count }

		return render_to_response('rango/about.html', context_dict, context)

def category(request, category_name_url):#set a page request url map for category names
	context = RequestContext(request) #requests context from the request sent to us
	# change underscores in category name to spaces
	#urls don handle spaces well, so we will encode them with spaces again to get the name
	#then we can replace the underscores with spaces again to get the name. 
	category_name = decodeUrl(category_name_url)
	print category_name
	#create context dictionary which we can pass to template redering engine
	#we start by containing the name of the category passes by the user
	context_dict = {'category_name' : category_name, 'category_name_url': category_name_url}

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

def project_info(request, project_name_url):#set a page request url map for category names
	context = RequestContext(request) #requests context from the request sent to us
	project_name = decodeUrl(project_name_url)
	context_dict = {'project_name' : project_name, 'project_name_url': project_name_url}

	try:
		#can we find the category with the given name
		#if we cant the .get() method raises a DoesNotExist exception.
		#so the .get() method returnes one model instance or raises the exception\\\
		project = Project.objects.get(name=project_name)
		context_dict['project'] = project
		#we also add the category object from db to context dict. 
		#and use this in the template to verify that the category exists. 
	except Project.DoesNotExist:
		#we get her if we can not find the category
		#we dont do anything - template displays no category message
		pass
	#got to render the resp.  and send to client
	return render_to_response('rango/project_info.html', context_dict, context)	

@login_required
def add_category(request):
	#get context of request
	context = RequestContext(request)
	#a http post?
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		# is the form we have valid
		if form.is_valid():
			#save new category into db
			form.save(commit=True)
			#call index view and user will be shown the homepage
			return index(request)
		else:
			#form had errors print to term
			print form.errors
	else:
		#if it is not a post display the form to enter details
		form = CategoryForm()

	return render_to_response('rango/add_category.html', {'form' : form}, context)

@login_required
def add_page(request, category_name_url):
	context = RequestContext(request)
	category_name = decodeUrl(category_name_url)

	if request.method == 'POST':
		form = PageForm(request.POST)

		if form.is_valid():
			page = form.save(commit=False)

			try:
				cat = Category.objects.get(name=category_name)
				page.category = cat

			except Category.DoesNotExist:
				render_to_response('rango/add_category.html')

			page.views = 0
			page.save()

			return category(request, category_name_url)

		else:
			print form.errors
	else:
		form = PageForm()

	return render_to_response('rango/add_page.html', {'category_name_url': category_name_url, 'category_name': category_name, 'form': form}, context)

@login_required
def add_project(request):
	context = RequestContext(request)
	
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		print form
		if form.is_valid():

			project = form.save(commit=False)
			project.creator = request.user
			project.save()


			return project_info(request, project_name_url)

		else:
			print form.errors
			print request.user

	else:
		form = ProjectForm()

	return render_to_response('rango/add_project.html', {'form' : form}, context)



def register(request):
	if request.session.test_cookie_worked():
		print "TEST SESSION WORKS"
		request.session.delete_test_cookie()


	context = RequestContext(request)
	registered = False #initial is set to false

	
	if request.method == 'POST':
		#grab info from form raw
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		#if both are valid

		if user_form.is_valid() and profile_form.is_valid():
			#save user form for DB
			user = user_form.save()
			#now hash pw
			user.set_password(user.password)
			user.save()
            
            #now we can save
			profile = profile_form.save(commit=False)
			profile.user = user

            #did they provide a pic	?

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
            #now save profile model instance
			profile.save()

            #update registry
			registered = True

		else:
			print user_form.errors, profile_form.errors

	else: 
		user_form = UserForm()
		profile_form = UserProfileForm()
	return render_to_response(
		'rango/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}, context)



def user_login(request):	
	context = RequestContext(request)

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		#lets see if the combo is valid
		user = authenticate(username=username, password=password)

		#if user exisits and details are correct
		if user is not None:

			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/rango/')

			else:
				return HttpResponse("Your account is disabled")
		else:
			 print "Invalid login detials were provided"
			 return HttpResponse("Invalid login detials supplied.")
	else:
		return render_to_response('rango/login.html', {}, context)

def restricted(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('rango/restricted.html', context_dict, context)

def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/rango/')

def event_page(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('rango/events.html', context_dict, context)

def fuck_bootstrap(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('rango/bootstraptest.html', context_dict, context)