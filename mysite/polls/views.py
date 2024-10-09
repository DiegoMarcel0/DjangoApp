from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.template import loader

from .models import Question

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
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does no exist")
    return render(request, "polls/detail.html", {"question": question})
    #return HttpResponse("La pregunta es: %s"%question_id)

def results(request, question_id):
    response = "Estas viendo los resultados de las preguntas %s"
    return HttpResponse(response%question_id)

def vote(request, question_id):
    return HttpResponse("Estas respondiendo la pregunta %s"% question_id)
