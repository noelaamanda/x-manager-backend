from django.contrib import admin

# Register your models here.
from .models import Message, Chat, Profile, Documents

admin.site.register(Message)
admin.site.register(Chat)
admin.site.register(Profile)
admin.site.register(Documents)