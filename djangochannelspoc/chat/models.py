from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ChatRoom(models.Model):
    room_name = models.CharField(max_length=100,unique=True)
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver')
    doc = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_name+'-'+str(self.sender.username)+'-'+str(self.receiver.username)


class Message(models.Model):
    room = models.ForeignKey(ChatRoom,on_delete=models.CASCADE)
    message = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_message')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_message')
    doc = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sender.username)+'-'+str(self.receiver.username)