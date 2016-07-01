from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
# import csv
#from django.template import loader

from .models import Question, Choice

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""Return the last five published questions."""
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

# def index(request):
# 	latest_question_list = Question.objects.order_by('-pub_date')[:5]
# 	#template = loader.get_template('polls/index.html')
# 	context = {
# 		'latest_question_list': latest_question_list,
# 	}
# 	# output = ', '.join([q.question_text for q in latest_question_list])
# 	return render(request, 'polls/index.html', context)

# def detail(request, question_id):
# 	question = get_object_or_404(Question, pk=question_id)
# 	return render(request, 'polls/detail.html', {'question': question})

# def results(request, question_id):
# 	question = get_object_or_404(Question, pk=question_id)
# 	return render(request, 'polls/results.html', {'question':question})
@csrf_exempt 
def voteManual(request, question_id):
	json_data = json.loads(request.body)
	question = get_object_or_404(Question, pk=json_data['question_id'])

	try:
		selected_choice = question.choice_set.get(pk=json_data['choice'])
	except (KeyError, Choice.DoesNotExist):
		print(KeyError)
	else: 
		selected_choice.votes += 1
		selected_choice.save()

@csrf_exempt
def voteAndroid(request, question_id):
	json_data = json.loads(request.body)
	question = get_object_or_404(Question, pk=json_data['question_id'])

	try:
		selected_choice = question.choice_set.get(pk=json_data['choice'])
	except (KeyError, Choice.DoesNotExist):
		print(KeyError)
	else: 
		selected_choice.votes += 1
		selected_choice.save()

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	print(request)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		print(KeyError)
		#show voting form again
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice."
			})
	else: 
		selected_choice.votes += 1
		selected_choice.save()
	return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))

