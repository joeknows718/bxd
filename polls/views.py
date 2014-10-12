from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,  get_object_or_404 
from django.template import RequestContext, loader
from polls.models import Poll
from django.core.urlresolvers import reverse



def index(request):
	latest_poll_list = Poll.objects.order_by('pub_date')[:5]
	template = loader.get_template('polls/index.html')
	context = RequestContext(request, {
		'latest_poll_list' : latest_poll_list
		})
	return HttpResponse(template.render(context))

def detail(request, poll_id):
	poll = get_object_or_404(Poll, pk=poll_id )
	return render(request, '/polls/detail.html', {'poll' : poll}  )

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question': question})

	

def vote(request, poll_id):
	p = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, ChoiceDoesNotExist):
		return render(request, 'poll/detial.html', {'question': p, 'error_message' : "You didn't select a choice.",})

	else:
		selected_choice.votes += 1
		selected_choice.save()

		return HttpResponseRedirect(reverse('polls:results', args=(p.id)))	



