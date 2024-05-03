from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='todos', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Create your models here.
