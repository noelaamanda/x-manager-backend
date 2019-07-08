from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.contrib.postgres.fields import ArrayField

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    identityKey = models.CharField(max_length=500, blank = True)
    registrationId = models.CharField(max_length=500, blank = True)
    keys = ArrayField(ArrayField(models.CharField(max_length=500, blank=True, null=True),
                              null=True), null=True) 

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, created, **kwargs):
        instance.profile.save()

class Message(models.Model):
    author = models.ForeignKey(User, related_name='messages', on_delete = models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.author.username

class Chat(models.Model):
    participants = models.ManyToManyField(Profile, related_name = 'chats')
    messages = models.ManyToManyField(Message, blank = True)
    isGroup = models.BooleanField(default = False)
    name = models.CharField(blank = True, max_length=50)
    def get_current_chat(chatId):
        return get_object_or_404(Chat, id=chatId)

    def last_10_messages(chatId):
        chat = Chat.objects.filter(id=chatId).first()
        if chat is not None:
            return chat.messages.order_by('-timestamp').all()[:10]
        else:
            return chat

    def createchat(request):
        chat = Chat.objects.create(
            participants = request.data.get('participants'),
            isGroup = request.data.get('isGroup'),
            name= request.data.get('name')
        )
        chat.save()
        return ('ok')

    def __str__(self):
        return "{}".format(self.pk)

class Documents(models.Model):
    author = models.ForeignKey(User, related_name="userdocs",on_delete = models.CASCADE)
    chatdoc = models.ForeignKey(Chat, related_name="docs", on_delete = models.CASCADE)
    file = models.FileField(upload_to='docs/%Y/%m/%d/')


    def __str__(self):
        return self.file.name