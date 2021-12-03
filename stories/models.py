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
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        if not self.step.prompt:
            text ='Once upon a time' + self.proposal_text 
        else:
            text = self.proposal_text
        return text

    def story_url(self):
        return self.step.story_url()

    def formatted_prompt(self):
        thoughts = self.thoughts.all()
        story_title = self.step.story.title 
        story_text = self.step.prompt
        prompt = ""
        if len(thoughts) == 0 and not story_text:
            prompt += f"#{story_title}\n"
        elif len(thoughts) > 0:
            prompt = "Write a story using this information:\n"
            prompt += f"The story is titled {story_title}"
            for thought in thoughts:
                prompt += f"- {thought}\n"
            prompt += '\n'
        prompt += story_text or 'Once upon a time'
        return prompt


class Thought(models.Model):
    proposal = models.ForeignKey(Proposal, related_name='thoughts', on_delete=models.CASCADE)
    thought_text = models.CharField(max_length=200, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.thought_text
