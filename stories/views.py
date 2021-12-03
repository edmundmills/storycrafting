from typing import Any, Dict

from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Story, Step, Proposal, Thought
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
        context.update({
            'steps_list': self.object.steps.all().order_by('-id'),
            'proposal': self.object.current_proposal,
            'thought_list': self.object.current_proposal.thoughts.all(), 
        })
        return context

def prompt(request, pk):
    proposal = get_object_or_404(Proposal, id=pk)
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
    accepted_text = proposal.proposal_text
    if not step.prompt:
        accepted_text = 'Once upon a time' + accepted_text
    step = Step.objects.create(story_id=step.story_id, prompt=accepted_text)
    Proposal.objects.create(step_id=step.id)
    return HttpResponseRedirect(step.story_url())

def reject_proposal(request, pk):
    proposal = get_object_or_404(Proposal, id=pk)
    new_proposal = Proposal.objects.create(step_id=proposal.step_id)
    for thought in proposal.thoughts.all():
        thought.id = None
        thought.proposal_id = new_proposal.id
        thought.save()
    return HttpResponseRedirect(new_proposal.story_url())

def add_thought(request, pk):
    proposal = get_object_or_404(Proposal, id=pk)
    print(request.POST)
    text = request.POST['thought_text']
    Thought.objects.create(proposal_id=proposal.id, thought_text=text)
    story = proposal.step.story
    return HttpResponseRedirect(story.get_absolute_url())

def delete_thought(request, pk):
    thought = get_object_or_404(Thought, id=pk)
    thought.delete()
    proposal = thought.proposal
    return HttpResponseRedirect(proposal.story_url())


