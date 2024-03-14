from django.shortcuts import render
from django.http import HttpResponse,Http404,JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import (ProfileSerializer,Profile,UserSerializer,User,RoomSerializer,Room,Message,MessageSerializer)
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
# Create your views here.

class profileViewSet(APIView):
    permission_classes = [IsAuthenticated, ]
    """
    use: users/user_id to get a specific user
    other routes: rooms/all, rooms/all?q=<id> replace <id> with the desired id to get a specific room

    """
    def get(self,request):
        query = Profile.objects.all()
        serializer = ProfileSerializer(query, many=True)
        return Response(serializer.data)
    def post(self,request,format=None):
        data = request.POST['data']
        serializer = ProfileSerializer(data=data)
        return HttpResponse("posted  successfuly")
    
class roomViewSet(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self,request):
        print(request.query_params.get('q','notfound'))
        if request.query_params.get('id'):
            query = Room.objects.get(pk=request.query_params.get('id'))
            serializer = RoomSerializer(query)
            return Response(serializer.data)
        else:
            query = Room.objects.all()
            serializer = RoomSerializer(query,many=True)
            return Response(serializer.data)

class messageViewSet(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self,request):

        if request.query_params.get('id'):
            query = Message.objects.get(pk=request.query_params.get('id'))
            serializer = MessageSerializer(query)
            return Response(serializer.data)
        else:
            if request.query_params.get('l'):
                num_of_messages = request.query_params.get('l') 
                query = Message.objects.all()[:int(num_of_messages)]
            else:
                query = Message.objects.all()
            serializer = MessageSerializer(query,many=True)
            return Response(serializer.data)
    
    def post(self,request):

        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200,message="created successfuly")
        else:
            return Response(status=400,message='invalid data')


class Login_User(APIView):
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        search_user = User.objects.get(email=email)
        user = authenticate(request,username=search_user.username,password=password)
        if user is not None:
            login(request,user)
            serializer = UserSerializer(search_user)
            return Response({'message':'successfully loged in','user':serializer.data},status=200)
        else:
            return Response({'message':'no user found with this emeil'},status=404)
        # print(email, password)
        # return HttpResponse('gyyy')
        
@method_decorator(ensure_csrf_cookie, name='dispatch')
class get_csrfToken(APIView):
    def get(self,request):
        return Response({'message':'success'})
    