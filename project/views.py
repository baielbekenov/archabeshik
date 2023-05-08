from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import User, Comment
from rest_framework import generics
from project.models import Category, Content, HouseManage, User
from project.serializers import CategorySerializer, ContentSerializer, HouseManageSerializer, UserSerializer, \
    CommentSerializer
from .pagination import CommentPagination, CategoryPagination, ContentPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'status': 403, 'errors': serializer.errors, 'messge': 'Something went wrong'})
        serializer.save()

        user = User.objects.get(username = serializer.data['username'])
        token_obj, _ = Token.objects.get_or_create(user=user)

        return Response({'status': 200, 'payload': serializer.data, 'token': str(token_obj), 'messge': 'your data is saved'})


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class CheckAuthAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({'detail': 'Authenticated.'})


class CategoryCreateAPIView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


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


class ContentSearchAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        search_query = request.GET.get('seach', '')
        queryset = Content.objects.filter(name__icontains=search_query)
        serializer = ContentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_302_FOUND)


class Contentlist(APIView):
    serializer_class = ContentSerializer
    permission_classes = [AllowAny]

    def get(self, request, category):
        queryset = Content.objects.filter(category_id=category)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class ContentCreate(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class ContentDelete(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, pk):
        try:
            obj = Content.objects.get(pk=pk)
        except Content.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            # и другие данные пользователя, которые нужно вернуть
        })


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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = HouseManage.objects.all()
    serializer_class = HouseManageSerializer
    permission_classes = [IsAuthenticated, ]


class HouseManageListAPIView(generics.ListAPIView):
    queryset = HouseManage.objects.all()
    serializer_class = HouseManageSerializer
    permission_classes = [AllowAny]


class HouseManageRetrive(generics.RetrieveAPIView):
    queryset = HouseManage.objects.all()
    serializer_class = HouseManageSerializer
    permission_classes = [AllowAny]
