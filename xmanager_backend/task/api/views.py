from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView
)
from task.models import Tasks, Projects
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import TaskSerializer, ProjectSerializer
from django.contrib.auth.models import User
import datetime 

User = get_user_model()


def get_user_contact(username):
    user = get_object_or_404(User, username = username)
    #contact = get_object_or_404(Profile, user = user)
    return user


class TaskListView(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        queryset = Tasks.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            contact = get_user_contact(username)
            queryset = contact.task.all()
        return queryset

class TaskDetailView(RetrieveAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.AllowAny, )

class TaskCreateView(CreateAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.AllowAny, )


class TaskUpdateView(UpdateAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.AllowAny, )

class TaskDeleteView(DestroyAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.AllowAny, )

