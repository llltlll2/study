from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView
from .models import Goal, StudyRecord
from .services import evaluate_progress
from django import forms
from django.utils import timezone

class GoalCreateView(CreateView):
    model = Goal
    fields = ['title', 'target_hours', 'start_date', 'end_date']
    template_name = 'tracker/goal_form.html'

    def get_success_url(self):
        return reverse('tracker:goal_detail', kwargs={'pk': self.object.pk})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['start_date'].widget = forms.DateInput(attrs={'type': 'date'})
        form.fields['end_date'].widget = forms.DateInput(attrs={'type': 'date'})
        return form

class GoalDetailView(DetailView):
    model = Goal
    template_name = 'tracker/goal_detail.html'
    context_object_name = 'goal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        goal = self.object
        context['progress'] = evaluate_progress(goal)
        context['records'] = goal.records.order_by('-studied_at')
        return context

class StudyRecordCreateView(CreateView):
    model = StudyRecord
    fields = ['studied_at', 'duration', 'comment']
    template_name = 'tracker/record_form.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['studied_at'] = timezone.now()
        return initial

    def form_valid(self, form):
        goal = get_object_or_404(Goal, pk=self.kwargs['goal_id'])
        form.instance.goal = goal
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracker:goal_detail', kwargs={'pk': self.kwargs['goal_id']})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['studied_at'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        return form
