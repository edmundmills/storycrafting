from django.contrib import admin
from .models import Story, Step, Thought, Proposal
# Register your models here.

admin.site.register(Story)
admin.site.register(Step)
admin.site.register(Thought)
admin.site.register(Proposal)