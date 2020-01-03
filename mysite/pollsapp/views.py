from django.shortcuts import render, get_object_or_404
from django.template import loader

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice

def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")

    # latest_question_list = Question.objects.all()
    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)

    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('pollsapp/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    # return HttpResponse("You're looking at question %s." % question_id)
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'pollsapp/detail.html', {'question': question})

def results(request, question_id):
    # response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'pollsapp/results.html', {'question': question})

def vote(request, question_id):  
     question = get_object_or_404(Question, pk=question_id)
    # return HttpResponse("You're voting on question %s." % question_id)    
     try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
     except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'pollsapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
     else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('pollsapp:results', args=(question.id,)))
