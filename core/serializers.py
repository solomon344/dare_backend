from rest_framework.serializers import ModelSerializer
from .models import Profile,User,Room,Message


class ProfileSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Profile

class UserSerializer(ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        fields = ['first_name','last_name','email','id','username','profile']
        model = User

class RoomSerializer(ModelSerializer):
    members = UserSerializer(many=True)
    created_by = UserSerializer()
    class Meta:
        fields = '__all__'
        model = Room

class MessageSerializer(ModelSerializer):
    by = UserSerializer()
    room = RoomSerializer()
    class Meta:
        fields = '__all__'
        model = Message