from rest_framework import serializers
from task.models import Tasks, Projects
from django.contrib.auth.models import User 

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ('__all__')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = "__all__"