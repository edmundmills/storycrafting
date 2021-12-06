from django import forms

from .models import Story

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ('title',)
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(forms.ModelForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data=super(forms.ModelForm, self).clean()
        cleaned_data['author_id'] = self.user.id
        return cleaned_data
