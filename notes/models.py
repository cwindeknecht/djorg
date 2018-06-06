from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

# Create your models here.

class Note(models.Model):
    note_id = models.CharField(primary_key=True, default=uuid4, editable=False, max_length=36)
    title = models.CharField(max_length=200, default='')
    content = models.TextField(blank=True, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=200, default='')