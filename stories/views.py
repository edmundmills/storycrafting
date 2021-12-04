from typing import Any, Dict

from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Story, Step, Proposal, Thought, Fact
from .services.prompter import Prompter

class IndexView(generic.ListView):
    template_name = 'stories/index.html'
    context_object_name = 'stories'

    def get_queryset(self):
        return Story.objects.all()

class NewView(generic.edit.CreateView):
    template_name = 'stories/new.html'
    model = Story
    fields = ['title']

    def form_valid(self, *args, **kwargs):
        response = super().form_valid(*args, **kwargs)
        step = Step.objects.create(story_id=self.object.id)
        Proposal.objects.create(step_id=step.id)
        return response

class WriteView(generic.edit.UpdateView):
    template_name = 'stories/write.html'
    model = Story
    fields = []

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        current_proposal = self.object.current_proposal
        context.update({
            'steps_list': self.object.steps.all().order_by('-id'),
            'proposal': current_proposal,
            'thought_list': current_proposal.thoughts.all(),
            'fact_list': current_proposal.facts.all(),
            'editable': not current_proposal.proposal_text,
        })
        return context

class ReadView(generic.DetailView):
    template_name = 'stories/read.html'
    model = Story

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'steps_list': self.object.steps.all().order_by('-id'),
        })
        return context

def prompt(request, pk):
    proposal = get_object_or_404(Proposal, id=pk)
    proposal.thoughts.all().delete()
    proposal.facts.all().delete()
    
    thoughts_text = request.POST['thoughts_text']
    thoughts = thoughts_text.split('\n')
    for thought_string in thoughts:
        Thought.objects.create(proposal_id=proposal.id, thought_text=thought_string)
    facts_text = request.POST['facts_text']
    facts = facts_text.split('\n')
    for fact_string in facts:
        Fact.objects.create(proposal_id=proposal.id, fact_text=fact_string)

    formatted_prompt = proposal.formatted_prompt()
    response = Prompter.prompt(formatted_prompt)
    proposal.proposal_text = response
    proposal.save()
    return HttpResponseRedirect(proposal.story_url())

def accept_proposal(request, pk):
    proposal = get_object_or_404(Proposal, id=pk)
    step = proposal.step
    proposal.accepted = True
    proposal.save
    accepted_text = str(proposal)
    step = Step.objects.create(story_id=step.story_id, prompt=accepted_text, accepted_proposal_id=proposal.id)
    new_proposal = Proposal.objects.create(step_id=step.id)
    for fact in proposal.facts.all():
        fact.id = None
        fact.proposal_id = new_proposal.id
        fact.save()
    return HttpResponseRedirect(step.story_url())

def edit_proposal(request, pk):
    proposal = get_object_or_404(Proposal, id=pk)
    text = request.POST['proposal_text']
    proposal.proposal_text = text
    proposal.save()
    return HttpResponseRedirect(proposal.story_url())

def reject_proposal(request, pk):
    proposal = get_object_or_404(Proposal, id=pk)
    new_proposal = Proposal.objects.create(step_id=proposal.step_id)
    for thought in (*proposal.thoughts.all(), *proposal.facts.all()):
        thought.id = None
        thought.proposal_id = new_proposal.id
        thought.save()
    return HttpResponseRedirect(new_proposal.story_url())



