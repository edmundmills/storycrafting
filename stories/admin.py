from django.contrib import admin
from .models import Story, Step, Thought, Proposal

admin.site.register(Story)

class ProposalInline(admin.StackedInline):
    model = Proposal

class ThoughtInline(admin.StackedInline):
    model = Thought

class StepAdmin(admin.ModelAdmin):
    inlines = [ProposalInline]

admin.site.register(Step, StepAdmin)
