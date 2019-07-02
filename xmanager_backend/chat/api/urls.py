from django.urls import path, re_path
from .views import (
    ChatCreateView,
    ChatDeleteView,
    ChatDetailView,
    ChatListView,
    ChatUpdateView,
    UserListView,
    FileUploadView
)
"""app_name = 'chat'"""

urlpatterns = [
   path('create/', ChatCreateView.as_view()),
   path('', ChatListView.as_view()),
   path('<pk>', ChatDetailView.as_view()),
   path('<pk>/update/', ChatUpdateView.as_view()),
   path('<pk>/delete/', ChatDeleteView.as_view()),
   path('users/', UserListView.as_view()),
   path('docs/', FileUploadView.as_view())
 ]
 