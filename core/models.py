from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from django.db import IntegrityError
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='media', blank=True, null=True)
    country = models.CharField(max_length=5,default='GM')

    def __str__(self):
        return self.user.username
    
class Room(models.Model):
    name = models.CharField(max_length=300)
    room_id = models.CharField(max_length=100, unique=True,default=''.join(str(uuid4()).split('-')[-1]+'-daregames'))
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='rooms')
    isprivate = models.BooleanField(default=False)
    description = models.TextField(default="This is going to be an awesome dare game")
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name

class Message(models.Model):
    message = models.CharField(max_length=500)
    by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='messages')
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    created_time = models.TimeField(auto_now_add=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.by.username
