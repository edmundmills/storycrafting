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

class Step(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    prompt = models.CharField(max_length=200, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.story} Step {self.id}"

class Proposal(models.Model):
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    proposal_text = models.CharField(max_length=200, default='')
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.proposal_text

class Thought(models.Model):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    thought_text = models.CharField(max_length=200, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.thought_text
