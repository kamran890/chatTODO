import uuid
from django.db import models
from django.utils import timezone


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='medium')
    category = models.CharField(max_length=50)
    due_date = models.DateTimeField()
    estimated_time = models.PositiveIntegerField(help_text="Estimated time in minutes")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['due_date']

    def is_overdue(self):
        """Check if the task is overdue based on the current time and due date."""
        return self.due_date < timezone.now() and self.status != 'completed'

    def update_status(self):
        """Update the task status to overdue if it’s past the due date."""
        if self.is_overdue():
            self.status = 'overdue'
            self.save()
