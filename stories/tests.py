from django.test import TestCase
from django.urls import reverse

from .models import Story

def create_story(**kwargs):
    return Story.objects.create(**kwargs)

class StoryIndexViewTests(TestCase):
    def test(self):
        response = self.client.get(reverse('stories:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New Story")

class StoryNewViewTests(TestCase):
    def test(self):
        response = self.client.get(reverse('stories:new'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New Story")

class StoryWriteViewTests(TestCase):
    def test(self):
        story = create_story(title='Test Story')
        response = self.client.get(reverse('stories:write', args=(story.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, story.title)

