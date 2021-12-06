from django.db import models
from django.urls import reverse



class Story(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('stories:write', args=[self.id])

    @property
    def current_step(self):
        return self.steps.order_by('-id')[0]

    @property
    def current_proposal(self):
        step = self.current_step
        return step.proposals.order_by('-id')[0]

class Step(models.Model):
    story = models.ForeignKey(Story, related_name='steps', on_delete=models.CASCADE)
    prompt = models.CharField(max_length=1000, default='')
    previous_proposal = models.OneToOneField('Proposal', null=True, on_delete=models.SET_NULL, related_name='next_step')
    generated_context = models.CharField(max_length=1000, default='')
    accepted_context = models.CharField(max_length=1000, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.story} Step {self.id}"

    def story_url(self):
        return reverse('stories:write', args=[self.story_id])


class Proposal(models.Model):
    step = models.ForeignKey(Step, related_name='proposals', on_delete=models.CASCADE)
    proposal_text = models.CharField(max_length=1000, default='')
    context_text = models.CharField(max_length=1000, default='')
    reasoning_text = models.CharField(max_length=1000, default='')
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.proposal_text

    def story_url(self):
        return self.step.story_url()

    @property
    def facts(self):
        return self.context_text.split('\n') if self.context_text else []
    
    @property
    def thoughts(self):
        return self.reasoning_text.split('\n') if self.reasoning_text else []
