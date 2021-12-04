from django.test import TestCase
from django.urls import reverse

from .models import Story, Step, Proposal

def create_story(**kwargs):
    story = Story.objects.create(**kwargs)
    step = Step.objects.create(story_id=story.id)
    Proposal.objects.create(step_id=step.id)
    return story

class StoryIndexViewTests(TestCase):
    def test(self):
        response = self.client.get(reverse('stories:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New Story")

class StoryNewViewTests(TestCase):
    def test_new(self):
        response = self.client.get(reverse('stories:new'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New Story")
    
    def test_create_valid(self):
        self.client.post(reverse('stories:new'), {'title': 'Test Story'})
        stories = Story.objects.all()
        self.assertEqual(len(stories), 1)
        steps = stories[0].steps.all()
        self.assertEqual(len(steps), 1)
        proposals = steps[0].proposals.all()
        self.assertEqual(len(proposals), 1)

    def test_create_no_title(self):
        self.client.post(reverse('stories:new'), {'title': ''})
        stories = Story.objects.all()
        self.assertEqual(len(stories), 0)

class StoryWriteViewTests(TestCase):
    def test(self):
        story = create_story(title='Test Story')
        response = self.client.get(reverse('stories:write', args=(story.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, story.title)

    def test_no_story(self):
        response = self.client.get(reverse('stories:write', args=(1,)))
        self.assertEqual(response.status_code, 404)

class StoryReadViewTests(TestCase):
    def test(self):
        story = create_story(title='Test Story')
        response = self.client.get(reverse('stories:read', args=(story.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, story.title)

    def test_no_story(self):
        response = self.client.get(reverse('stories:read', args=(1,)))
        self.assertEqual(response.status_code, 404)
