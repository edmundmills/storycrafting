from django.contrib import admin
from .models import Story, Step, Proposal

admin.site.register(Story)

class ProposalInline(admin.StackedInline):
    model = Proposal

class StepAdmin(admin.ModelAdmin):
    inlines = [ProposalInline]

admin.site.register(Step, StepAdmin)
