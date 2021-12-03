from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Story, Step, Proposal, Thought

class IndexView(generic.ListView):
    template_name = 'stories/index.html'
    context_object_name = 'stories'

    def get_queryset(self):
        return Story.objects.all()

class NewView(generic.edit.CreateView):
    template_name = 'stories/new.html'
    model = Story
    fields = ['title']

class WriteView(generic.edit.UpdateView):
    template_name = 'stories/write.html'
    model = Story
    extra_context = {
        'step_list': Step.objects.all(),
        'proposal': Proposal.objects.all().order_by('-id'),
        'thought_list': Thought.objects.all(),
    }
    fields = []
