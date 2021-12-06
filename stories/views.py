from typing import Any, Dict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Story, Step, Proposal
from .services.prompter import Prompter

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'stories/index.html'
    context_object_name = 'stories'

    def get_queryset(self):
        return Story.objects.all()

class NewView(LoginRequiredMixin, generic.edit.CreateView):
    template_name = 'stories/new.html'
    model = Story
    fields = ['title']

    def form_valid(self, *args, **kwargs):
        response = super().form_valid(*args, **kwargs)
        step = Step.objects.create(story_id=self.object.id)
        Proposal.objects.create(step_id=step.id)
        return response

class WriteView(LoginRequiredMixin, generic.edit.UpdateView):
    template_name = 'stories/write.html'
    model = Story
    fields = []

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        current_proposal = self.object.current_proposal
        context.update({
            'steps_list': self.object.steps.all().order_by('-id'),
            'proposal': current_proposal,
        })
        return context

class ReadView(LoginRequiredMixin, generic.DetailView):
    template_name = 'stories/read.html'
    model = Story

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'steps_list': self.object.steps.all().order_by('-id'),
        })
        return context

@login_required
def update_proposal(request, pk):
    proposal = get_object_or_404(Proposal, id=pk)
    step = proposal.step
    if 'proposal_text' in request.POST:
        proposal_text = request.POST['proposal_text'].strip()
    reasoning_text = request.POST['reasoning_text'].strip()
    context_text = request.POST['context_text'].strip()
    if 'generate_proposal' in request.POST:
        proposal.context_text = context_text
        proposal.reasoning_text = reasoning_text
        proposal.proposal_text = Prompter.generate_proposal(proposal)
    elif 'accept' in request.POST:
        proposal.proposal_text = proposal_text
        proposal.accepted = True
        proposal.save()
        step = Step.objects.create(story_id=step.story_id, prompt=proposal_text, previous_proposal_id=proposal.id)
        Proposal.objects.create(step_id=step.id)
        step.generated_context = Prompter.updated_context(step)
        step.save()
        return HttpResponseRedirect(reverse('stories:update_context', args=[step.id]))
    elif 'new_proposal' in request.POST:
        Proposal.objects.create(step_id=proposal.step_id,
                                context_text=context_text,
                                reasoning_text=reasoning_text)
    proposal.save()
    return HttpResponseRedirect(proposal.story_url())

class UpdateContextView(LoginRequiredMixin, generic.edit.UpdateView):
    template_name = 'stories/steps/update_context.html'
    model = Step
    fields = ['accepted_context']

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'story': self.object.story,
            'previous_facts_list': self.object.previous_proposal.facts,
        })
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        accepted_context = self.get_form_kwargs()['data']['accepted_context']
        proposal = self.object.proposals.all()[0]
        proposal.context_text = accepted_context
        proposal.save()
        return response

    def get_success_url(self):
        return self.object.story_url()

