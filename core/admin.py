from django.contrib import admin
from .models import (Profile,Room,Message)
# Register your models here.
admin.site.register(Profile)
admin.site.register(Room)
admin.site.register(Message)
