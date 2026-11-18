from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError

from config import settings
from customers.models import Customer


class Project(models.Model):
    class Status(models.TextChoices):
        PLANNED = 'planned', 'Planned'
        IN_PROGRESS = 'in_progress', 'In progress'
        ON_HOLD = 'on_hold', 'On hold'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name='projects')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PLANNED)
    deadline = models.DateField(null=True, blank=True)
    budget = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.CheckConstraint(condition=Q(
            budget__gte=0), name='project_budget_non_negative')]

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='project_assignments')
    is_lead = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('project', 'user'), name='unique_project_member'),
            models.UniqueConstraint(
                fields=('project',), condition=Q(is_lead=True), name='unique_project_lead')
        ]

    def __str__(self):
        return f'{self.user} - {self.project}'


class Task(models.Model):
    class Status(models.TextChoices):
        BACKLOG = 'backlog', 'Backlog'
        IN_PROGRESS = 'in_progress', 'In progress'
        IN_REVIEW = 'in_review', 'In review'
        DONE = 'done', 'Done'

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assignee = models.ForeignKey(
        ProjectMember, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_tasks')
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.BACKLOG)
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

    def clean(self):
        super().clean()
        if self.assignee is not None:
            if self.assignee.project != self.project:
                raise ValidationError(
                    {'assignee': 'The assignee must be a member of this project'})
