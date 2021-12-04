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
    accepted_proposal = models.OneToOneField('Proposal', null=True, on_delete=models.SET_NULL, related_name='next_step')
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

    @property
    def previous_proposal(self):
        return self.accepted_proposal

class Proposal(models.Model):
    step = models.ForeignKey(Step, related_name='proposals', on_delete=models.CASCADE)
    proposal_text = models.CharField(max_length=1000, default='')
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
    def facts_text(self):
        return "".join(f"{fact}\n" for fact in self.facts.all())

    @property
    def thoughts_text(self):
        return "".join(f"{thought}\n" for thought in self.thoughts.all())

    def update_facts(self, facts_text):
        self.facts.all().delete()
        facts = facts_text.split('\n')
        for fact_string in facts:
            fact_string = ' '.join(fact_string.split())
            if fact_string:
                if fact_string[0:2] == '- ':
                    fact_string = fact_string[2:]
                Fact.objects.create(proposal_id=self.id, fact_text=fact_string)

    def update_thoughts(self, thoughts_text):
        self.thoughts.all().delete()
        thoughts = thoughts_text.split('\n')
        for thought_string in thoughts:
            thought_string = ' '.join(thought_string.split())
            if thought_string:
                Thought.objects.create(proposal_id=self.id, thought_text=thought_string)



class Thought(models.Model):
    proposal = models.ForeignKey(Proposal, related_name='thoughts', on_delete=models.CASCADE)
    thought_text = models.CharField(max_length=200, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.thought_text

class Fact(models.Model):
    proposal = models.ForeignKey(Proposal, related_name='facts', on_delete=models.CASCADE)
    fact_text = models.CharField(max_length=200, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.fact_text
