from django.shortcuts import render, get_object_or_404
from django.template import loader

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice

def index(request):
   

    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('pollsapp/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
  
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'pollsapp/detail.html', {'question': question})

def results(request, question_id):
    
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'pollsapp/results.html', {'question': question})

def vote(request, question_id):  
     question = get_object_or_404(Question, pk=question_id)
   
     try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
     except (KeyError, Choice.DoesNotExist):
        
        return render(request, 'pollsapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
     else:
        selected_choice.votes += 1
        selected_choice.save()
       
        return HttpResponseRedirect(reverse('pollsapp:results', args=(question.id,)))
