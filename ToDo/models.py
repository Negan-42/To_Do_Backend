# models.py
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)  # Automatically set when created
    complete = models.BooleanField(default=False)  # Boolean for completion status
    order = models.PositiveIntegerField(default=0)  # Field to track task order

    def __str__(self):
        return self.title
