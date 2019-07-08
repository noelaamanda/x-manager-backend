from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# Create your models here.
User = get_user_model()

class Tasks(models.Model):
    participants = models.ManyToManyField(User, related_name = 'task')
    name = models.CharField(blank=False, max_length=50)
    created = models.TimeField(auto_now_add=True)
    estimation = models.DurationField()
    start = models.TimeField()


class Projects(models.Model):
    participants = models.ManyToManyField(User, related_name = 'project')
    name = models.CharField(blank=False, max_length=50)