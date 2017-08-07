from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect , HttpResponse
from django.core.urlresolvers import reverse
from polls.models import Question,Choice
from django.views.generic import ListView , DetailView

import logging
logger = logging.getLogger(__name__)

class IndexView(ListView):
		template_name = 'polls/index.html'
		context_object_name = 'latest_question_list'

		def get_queryset(self):
				return Question.objects.order_by('-pub_date')[:5]

class DetailView(DetailView):
		model = Question
		template_name = 'polls/detail.html'


class ResultsView(DetailView):
		model = Question
		template_name = 'polls/results.html'

# Create your views here.
def vote(req,question_id):
		logger.debug("vote().question_id: %s" % question_id)
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

