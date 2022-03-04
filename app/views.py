from functools import partial
import imp
from django.shortcuts import render
from django.contrib.auth.models import User
from matplotlib.style import use
from numpy import delete
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.http import *
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status

class Register(APIView):
    def get(self,request):
        stu = Post.objects.all()
        serializer = PostSerializer(stu, many=True)
        permission_classes = [AllowAny]
        return Response(serializer.data)

    def post(self,request):
         username=request.data.get('username')
         password=request.data.get('password')
         user=User.objects.create(username=username)
         user.set_password(password)
         user.save()
         refresh = RefreshToken.for_user(user)
         return Response({'Status':'You have registered successfully','RefreshToken':str(refresh),'AccessToken':str(refresh.access_token)})

class Login(APIView):
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            return Response({'Msg':'You have loged in'})
        return Response({'Msg':'Enter valid username or password'})

class Profile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        stu = User.objects.filter(id = user.id)
        serializer = UserSerilizer(stu, many=True)
        return Response(serializer.data)

    def put(self,request):
        user = request.user
        stu = User.objects.get(id = user.id)
        serializer = UserSerilizer(stu, data=request.data,partial=True)
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        user = request.user
        stu = User.objects.get(id = user.id)
        stu.delete()
        return Response({'Msg':'User has deleted'})

class PostView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        stu = Post.objects.filter(user=user)
        serializer = PostSerializer(stu, many=True)
        return Response(serializer.data)

    def post(self,request,pk):
        stu = Post.objects.create(user= request.user,)
        serializer = PostSerializer(instance=stu,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'Post':'Post Successfully'})
        return Response({'Msg':'Somthing went wrong'})

    def put(self,request,pk):
        stu = Post.objects.filter(user = request.user)
        serializer = PostSerializer(instance=stu,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Post':'Updated'})
        return Response({'Msg':'Somethig went wrong'})

    def delete(self,request):
        user = request.user
        data = request.data
        stu = Post.objects.filter(id = data.get('id'),user=user)
        stu.delete()
        return Response({'Post':'Successfully Deleted'})

class Like(APIView):
    def get(self,request):
        stu = PostLike.objects.get(post = request.data.get('post'), like=True)
        count = stu.str(count())
        serializer = LikeSerializer(stu,many=True)
        return Response({'Data':serializer.data, 'Count':count})

class Comment(APIView):
    def get(self,request):
        data = request.data
        stu = PostComment(post_id = data.get('post'))
        count = stu.count()
        serializer = CommentSerializer(stu,many=True)
        return Response({'data':serializer.data,'count':count})

class PostComments(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        stu = PostComment.objects.create(user = request.user)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Msg':'Comment successfully posted'})
        return Response(serializer.errors)

    def put(self,request,pk):
        user = request.user
        data = request.data
        stu = PostComment.objects.get(user = user,post_id=data.get('post'))
        serializer = UserSerilizer(instance=stu,data = request.data,partial=True)
        if serializer.is_valid():
            return Response({'Msg':'Comment Updated'})
        return Response({'Msg':'Somthing went wrong'})

    def delete(self,request):
        user = request.user
        data = request.data
        stu = User.objects.filter(user=user,post_id=request.data('post'))
        stu = delete()
        return Response({'Msg':'Deleted'})

class SendRequest(APIView):
    permission_classe = [IsAuthenticated]
    def get(self,request):
        user = request.user
        stu = FriendRequest.objects.filter(user_from=False)
        serializer = RequestSerializer(stu,many=True)
        return Response(serializer.data)

    def post(self,request):
        stu = FriendRequest.objects.get_or_create(user_to = request.user, user_from_id = request.data.get('user_from'))
        serializer = RequestSerializer(stu,many=True)
        return Response({'Msg':'Request has sent'})

    def delete(self,request):
        try:
            user_from=request.data.get('user_form')
            stu = FriendRequest.objects.filter(user_to=request.user,IsAccepted=user_from)
            stu.delete()
            return Response({'Msg':'Request has deleted'})
        except:
            return Response({'Msg':'Something went wrong'})

class AcceptRequest(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        stu = FriendRequest.objects.filter(user_from=request.user,IsAccepted=False)
        serializer = RequestSerializer(stu,many=True)
        return Response(serializer.data)

    def put(self,request):
        try:
            user_to_id=request.data.get('user_to_id')
            stu = FriendRequest.objects.filter(user_from=request.user,IsAccepted=user_to_id)
            stu.IsAccepted=True
            return Response({'Msg':'Request has accepted'})
        except Exception as e:
            return Response({'Error':str(e)})

    def delete(self,request):
        try:
            stu = FriendRequest.objects.filter(user_from=request.user,IsAccepted=False,user_to_id=request.data.get('user_from'))
            stu.delete()
            return Response({'Msg':'Request has no accepted'})
        except Exception as e:
            return Response({'Error':str(e)})
