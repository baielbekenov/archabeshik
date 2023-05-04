from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.reverse import reverse

from .models import User, Comment
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, permissions, renderers, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.parsers import JSONParser
from rest_framework import mixins
from rest_framework import generics
from project.permissions import IsOwnerOrReadOnly

from project.models import Category, Content, HouseManage, User
from project.serializers import CategorySerializer, ContentSerializer, HouseManageSerializer, UserSerializer, \
    CommentSerializer
from .pagination import CommentPagination, CategoryPagination, ContentPagination
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response(UserSerializer(user).data)
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'})


class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('-id')
    pagination_class = CategoryPagination
    permission_classes = [AllowAny]



class ContentDetail(generics.RetrieveAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        comments = Comment.objects.filter(content=instance)
        comments_serializer = CommentSerializer(comments, many=True)
        return Response({
            'content': serializer.data,
            # 'comments': comments_serializer.data
        })

    def post(self, request, *args, **kwargs):
        content = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(content=content)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentList(generics.ListAPIView):
    queryset = Content.objects.all().order_by('-id')
    serializer_class = ContentSerializer
    pagination_class = ContentPagination
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category_id']

    def get_queryset(self):
        queryset = Content.objects.all()
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset



class ContentCreate(generics.CreateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [AllowAny]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class CommentListAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all().order_by('-id')
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    pagination_class = CommentPagination

    def get_queryset(self):
        content_id = self.kwargs['content_id']
        return Comment.objects.filter(content_id=content_id)


class CommentDestroyAPIView(DestroyAPIView):
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    # lookup_field = 'id'



class HouseManageCreateAPIView(generics.CreateAPIView):
    queryset = HouseManage.objects.all()
    serializer_class = HouseManageSerializer
    permission_classes = [IsAuthenticated, ]


class HouseManageListAPIView(generics.ListAPIView):
    queryset = HouseManage.objects.all()
    serializer_class = HouseManageSerializer
    permission_classes = [AllowAny]







