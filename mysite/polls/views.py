from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.db.models import F
from django.urls import reverse
from .models import Question, Choice
from django.views import generic
from .forms import QuestionForm, ChoiceForm
#demostracion de hacer algo con vistas
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    #forma resumida conla que no importamos HttpResponse ni loader
    context = {"latest_question_list": latest_question_list,}
    return render(request, "ola.html", context) 

    #template = loader.get_template("polls/index.html")
    #context = {
    #    "latest_question_list": latest_question_list,
    #}
    #return HttpResponse(template.render(context, request))
    
    #output = ", ".join([q.question_text for q in latest_question_list])
    #return HttpResponse(output)
    
    #return HttpResponse("Hello, world. You're at the polls index.")

#demostracion de views y recibir parametros
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})
    #try:
    #    question = Question.objects.get(pk=question_id)
    #except Question.DoesNotExist:
    #    raise Http404("Question does no exist")
    #return render(request, "polls/detail.html", {"question": question})
    #return HttpResponse("La pregunta es: %s"%question_id)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question":question})
    #response = "Estas viendo los resultados de las preguntas %s"
    #return HttpResponse(response%question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk= question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html",{
            "question": question,
            "error_message": "No se selecciono nada :v",
        },)
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        #usar luego de un proceso exitoso con POST
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    #return HttpResponse("Estas respondiendo la pregunta %s"% question_id)

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name ="latest_question_list"
    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"



def question_form(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("polls:addQuestion"))
        else:
            message_error = "Formulario invalido"
    else:
        message_error = None
    form = QuestionForm()
    return render(request, 'polls/question_form.html', {'form':form, 'error_message': message_error})

def choices_form(request):
    if request.method == "POST":
        form = ChoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("polls:addChoice"))
        else:
            message_error = "Formulario invalido"
    else:
        message_error = None
    form = ChoiceForm()
    #form = QuestionForm()
    return render(request, 'polls/question_form.html', {'form':form, 'error_message': message_error})
