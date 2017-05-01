import json
import datetime
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import loader, RequestContext
from django.core import serializers
from django.http import Http404
from django.views import generic
import plotly.offline as opy
import plotly.graph_objs as go
from django.views.generic import TemplateView
from graphos.renderers import gchart, flot, highcharts
from votePlus.apps.polls.models import Question, Choice
from graphos.sources.simple import SimpleDataSource
from graphos.sources.model import ModelDataSource
from graphos.renderers.gchart import LineChart, BaseChart
# from . import models

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        returns the last five published questions
        :return: 
        """
        return Question.objects.filter(
                pub_date__lte=timezone.now()
                ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'



class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'




def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # redisplay the question voting form
        return render(request, 'polls/detail.html', {
        'question':p,
        'error_message': "you did not select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        values = json.dumps(selected_choice.votes)
        labels = json.dumps(selected_choice.choice_text)

        return HttpResponseRedirect(reverse('polls:results',args=(p.id,)), )


# class Graph(TemplateView):
#     template_name = 'polls/reports.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(Graph, self).get_context_data(**kwargs)
#
#         x = [-2,0,4]
#         y = [q**2-q+3 for q in x]
#
#         trace1 = go.Scatter(x=x, y=y, marker={'color':'red', 'symbol':104, 'size':"10"},
#                             mode="lines", _name='1st trace')
#
#         data = go.Data([trace1])
#         layout =go.Layout(title='meine data', xaxis={'title':'x1'}, yaxis={'title':'x2'})
#         figure = go.Figure(data=data, layout=layout)
#         div = opy.plot(figure, auto_open=False, output_type='div')
#
#         context['graph'] = div
#
#         return context


def chart_data(request):
    question = Question.objects.get(pk=2)
    choices = Choice.objects.filter(question=question)
    data_source = ModelDataSource(choices, fields=['choice_text','votes'])
    chart = highcharts.BarChart(data_source)
    context = {'chart':chart}
    return render(request, 'polls/reports.html', context)










