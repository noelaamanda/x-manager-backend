from django.urls import path, re_path
from .views import (
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    TaskListView,
    TaskUpdateView,   
)
"""app_name = 'Task'"""

urlpatterns = [
   path('create/', TaskCreateView.as_view()),
   path('', TaskListView.as_view()),
   path('<pk>', TaskDetailView.as_view()),
   path('<pk>/update/', TaskUpdateView.as_view()),
   path('<pk>/delete/', TaskDeleteView.as_view()),
 ]
 