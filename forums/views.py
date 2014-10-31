# Create your views here.
from django.core.urlresolvers import reverse
from bxd.settings import MEDIA_ROOT, MEDIA_URL
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from forums.models import Forum, Thread, Post 
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from forums.forms import ProfileForm
from django.contrib.auth.decorators import login_required

def index(request):
	#main listing
	forums = Forum.objects.all()
	return render_to_response("forum/list.html", dict(forums=forums, user=request.user))

def add_csrf(request, **kwargs):
	d = dict(user=request.user, **kwargs)
	d.update(csrf(request)) 
	return d 

def mk_paginator(request, items, num_items):
	##create and return pageinator
	paginator = Paginator(items, num_items)
	try: 
		page = int(request.GET.get("page", '1'))
	except ValueError:
		page = 1

	try: 
		items = paginator.page(page)
	except (InvalidPage, EmptyPage):
		items = paginator.page(paginator.num_pages)
	return items 

def forum(request, pk):
	##listing of the threads in this forum:
	threads = Thread.objects.filter(forum=pk).order_by("created")
	threads = mk_paginator(request, threads, 20)
	return render_to_response('forum/forum.html', add_csrf(request, threads=threads, pk=pk))

def thread(request, pk):
	##listing of posts in thread bruh,
	posts = Post.objects.filter(thread=pk).order_by("created")
	posts = mk_paginator(request, posts, 15)
	title = Thread.objects.get(pk=pk).title
	t = Thread.objects.get(pk=pk)
	return render_to_response("forum/thread.html", add_csrf(request, posts=posts, pk=pk, title=title, media_url=MEDIA_URL, forum_pk=t.forum.pk))

def post(request, ptype, pk):
	##display post form
	action = reverse("forums.views.%s" % ptype, args=[pk])
	if ptype == "new_thread":
		title = "Start new topic:"
		subject = ''
	elif ptype == "reply":
		title = "Reply:"
		subject = "Re:" + Thread.objects.get(pk=pk).title

	return render_to_response("forum/thread.html", add_csrf(request, subject=subject, action=action, title=title))

def new_thread(request, pk):
		##new thread
	p = request.POST
	if p["subject"] and p["body"]:
		forum = Forum.objects.get(pk=pk)
		thread = Thread.objects.create(forum=forum, title=p["subject"], creator=request.user)
		Post.objects.create(thread=thread, title=p["subject"], body=p["body"], creator=request.user)
		increment_post_counter(request)
	return HttpResponseRedirect(reverse("bxd.forums.views.forum", args=[pk]))

def reply(request, pk):
	##post a reply in thread G
	p = request.POST
	if p["body"]:
		thread = Thread.objects.get(pk=pk)
		post = Post.objects.create(thread=thread, title=p["subject"], body=p["body"], creator=request.user)
	return HttpResponseRedirect(reverse("forums.views.thread", args=[pk] + "?page=last"))

def increment_post_counter(request):
	profile = request.user.userprofile_set.all()[0]
	prolile.posts += 1
	profile.save()

@login_required
def profile(request, pk):
	##edit user profile 
	profile = UserProfile.objects.get(user=pk)
	img = None 

	if request.method == "POST":
		pf = ProfileForm(request.POST, request.FILES, instance=profile)
		if pf.is_valid():
			pf.save()
			#resize image under filename 
			imfn = pjoin(MEDIA_ROOT, profile.picture.name)
			im = PImage.open(imfn)
			im.thumbnail((160,160), PImage.ANTIALIAS)
			im.save(imfn, "JPEG")
		else:
			pf = ProfileForm(instance=profile)

		if profile.avatar:
			img = "/media/" + profile.avatar.name

		return render_to_response("forum/profile.html", add_csrf(request, pf=pf, img=img))










		


 





