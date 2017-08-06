from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect , HttpResponse
from django.core.urlresolvers import reverse
from polls.models import Question,Choice

# Create your views here.
def index(req):
		latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
		context = {'latest_question_list': latest_question_list}
		return render(req ,'polls/index.html',context)

def detail(req,question_id):
		question = get_object_or_404(Question, pk=question_id)
		return render(req, 'polls/detail.html',{'question':question})

def vote(req,question_id):
		p = get_object_or_404(Question, pk = question_id)
		try:
				selected_choice = p.choice_set.get(pk=req.POST['choice'])
		except (KeyError,Choice.DoesNotExist):
				return render(req,'polls/detail.html',{
								'question': p,
								'error_message':"U didn't select a choice",
								})
		else:
				selected_choice.votes += 1
				selected_choice.save()
				return HttpResponseRedirect(reverse('polls:results',args=(p.id,)))

def results(req,question_id):
		question = get_object_or_404(Question,pk=question_id)
		return render(req,'polls/results.html',{'question':question})
