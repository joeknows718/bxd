from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext 
from BXD.models import Category, Project, UserProfile
from BXD.models import Page	
from BXD.forms import CategoryForm
from BXD.forms import PageForm, UserForm, UserProfileForm, ProjectForm
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models	import User
from datetime import datetime
	

def index(request):
		#Request the context of the request
		#context contains info ei client machine detials
		request.session.set_test_cookie
		#Const. A dict. to pass to template engine as context
		#bold message dict. key is the same as bold message embedded in index BXD index.html
		category_list = Category.objects.order_by('likes')[:5] 
		page_list = Page.objects.order_by('views')[:5]#create a list of top 5 categories fro the Catefory model, and ordering list by number of likes
		context_dict = {'categories' : category_list, 'pages': page_list}#showing all categories listed and ordered to be placed in template 
		#return rendered response and send to client 
		#use shortcut funtion to simplify
		#the first parameter in this render respnse is the template that gets called

		return render(request,'BXD/index.html', context_dict)
		

def resources(request):

		category_list = Category.objects.order_by('likes')[:10]
		page_list = Page.objects.order_by('views')[:20]
		context_dict = {'categories' : category_list, 'pages': page_list}
		
		return render(request, 'BXD/resources.html', context_dict)

def projects(request):

	project_list =  Project.objects.order_by('likes')[:10]
	context_dict = {'projects' : project_list}
	return render(request, 'BXD/projects.html', context_dict)

def about(request):
	#return HttpResponse("<a href='/BronxDigital/'>BXD</a> Bronx Digital is a collaborative Community of Bronx based Coders")	
		if request.session.get('visits'):
			count = request.session.get('visits')
		else:
			count = 0
		context_dict = { 'visits' : count }

		return render(request, 'BXD/about.html', context_dict)

def category(request, category_name_slug):#set a page request url map for category names
	# change underscores in category name to spaces
	#urls don handle spaces well, so we will encode them with spaces again to get the name
	#then we can replace the underscores with spaces again to get the name. 
	#create context dictionary which we can pass to template redering engine
	#we start by containing the name of the category passes by the user
	context_dict = {}

	try:
		#can we find the category with the given name
		#if we cant the .get() method raises a DoesNotExist exception.
		#so the .get() method returnes one model instance or raises the exception\\\
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name'] = category.name 
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
	return render(request, 'BXD/category.html', context_dict)	

def project_info(request, project_name_slug):#set a page request url map for category names
	 #requests context from the request sent to us
	context_dict = {}

	try:
		#can we find the category with the given name
		#if we cant the .get() method raises a DoesNotExist exception.
		#so the .get() method returnes one model instance or raises the exception\\\
		project = Project.objects.get(project_name=project_name_slug)
		context_dict['project'] = project
		context_dict['project_name'] = project.project_name 
		#we also add the category object from db to context dict. 
		#and use this in the template to verify that the category exists. 
	except Project.DoesNotExist:
		#we get her if we can not find the category
		#we dont do anything - template displays no category message
		pass
	#got to render the resp.  and send to client
	return render(request, 'BXD/project_info.html', context_dict)	

@login_required
def add_category(request):
	#get context of request
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

	return render(request, 'BXD/add_category.html', {'form' : form})

@login_required
def add_page(request, category_name_slug):
	try:
		cat = Category.objects.get(slug=category_name_slug)

	except Category.DoesNotExist:

		cat = None


	if request.method == 'POST':
		form = PageForm(request.POST)

		if form.is_valid():
			if cat:
				page = form.save(commit=False)
				page.category = cat
				page.views = 0
				page.save()
				return category(request, category_name_slug)
		else:
			print form.errors
	else:
		form = PageForm()

	return render(request, 'BXD/add_page.html', {'category_name_slug': category_name_slug, 'category_name': cat, 'form': form})

@login_required
def add_project(request):
	
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		if form.is_valid():

			project = form.save(commit=False)
			project.creator = request.user
			project.save()


			return projects(request)
		else:
			print form.errors
			print request.user

	else:
		form = ProjectForm()

	return render( request,'BXD/add_project.html', {'form' : form})



def register(request):
	if request.session.test_cookie_worked():
		print "TEST SESSION WORKS"
		request.session.delete_test_cookie()

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
	return render( request, 'BXD/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})



def user_login(request):	

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		#lets see if the combo is valid
		user = authenticate(username=username, password=password)

		#if user exisits and details are correct
		if user:

			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/BXD/')

			else:
				return HttpResponse("Your account is disabled")
		else:
			 print "Invalid login detials were provided"
			 return HttpResponse("Invalid login detials supplied.")
	else:
		return render(request,'BXD/login.html', {})

def restricted(request):
	context = RequestContext(request)
	context_dict = {}
	return render(request,'BXD/restricted.html', context_dict)

def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/BXD/')

def event_page(request):
	context = RequestContext(request)
	context_dict = {}
	return render(request, 'BXD/events.html', context_dict)

@login_required
def profile(request):
	context_dict={}
	u = User.objects.get(username=request.user )

	try:
		up = UserProfile.objects.get(user=u)

	except:
		up = None 
		print up

	context_dict['user'] = u
	context_dict['userprofile'] = up
	return render(request,'BXD/profile.html', context_dict)

def track_url(request):
	page_id = None 
	url = '/BXD/'
	if request.method == 'GET':
		if 'page_id' in request.GET:
			page_id = request.GET['page_id']
			try: 
				page = Page.objects.get(id=page_id)
				page.views = page.views + 1
				page.save()
				url = page.url
			except:
				pass
	return redirect(url)

@login_required
def like_category(request):
	cat_id = None

	if request.method == 'GET':
		cat_id = request.GET('category_id')

	likes = 0
	if cat_id:
		category = Category.objects.get(id=int(cat_id))
		if category:
			likes = category.likes + 1 
			category.likes = likes
			category.save()

	return HttpResponse(likes)




# Create your views here.
