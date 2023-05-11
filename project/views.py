from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import User, Comment
from rest_framework import generics
from project.models import Category, Content, HouseManage, User
from project.serializers import CategorySerializer, ContentSerializer, HouseManageSerializer, UserSerializer, \
    CommentSerializer
from .pagination import CommentPagination, CategoryPagination, ContentPagination, HouseManagePagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})
        serializer.save()

        user = User.objects.get(username=serializer.data['username'], is_superuser=serializer.data['is_superuser'])
        token_obj, _ = Token.objects.get_or_create(user=user)

        return Response({'status': 200, 'payload': serializer.data,
                         'token': str(token_obj), 'is_superuser': user.is_superuser, 'message': 'your data is saved'})


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key, 'is_superuser': user.is_superuser},
                        status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


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
        return Response({
            'content': serializer.data,
        })

    def post(self, request):
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

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.query_params.get('search', None)

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        return queryset

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        search_query = request.query_params.get('search', None)
        if search_query:
            response.data['search_query'] = search_query

        return response


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
    pagination_class = ContentPagination

    def get(self, request, category):
        queryset = Content.objects.filter(category_id=category)
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def get_image(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)


class ContentCreate(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    # def post(self, request):
    #     serializer = ContentSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentDelete(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, pk):
        try:
            obj = Content.objects.get(pk=pk)
        except Content.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContentPatchView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, pk):
        try:
            obj = Content.objects.get(pk=pk)
        except Content.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ContentSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

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


class HouseManageCreateAPIView(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = HouseManageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HouseManageListAPIView(generics.ListAPIView):
    queryset = HouseManage.objects.all()
    serializer_class = HouseManageSerializer
    permission_classes = [AllowAny]
    pagination_class = HouseManagePagination

    def get_image(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)


class HouseManageRetrive(generics.RetrieveAPIView):
    queryset = HouseManage.objects.all()
    serializer_class = HouseManageSerializer
    permission_classes = [AllowAny]

    # def get(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     comments = Comment.objects.filter(content=instance)
    #     return Response({
    #         'content': serializer.data,
    #     })

    def get_image(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)


class HouseManagePatch(APIView):

    def patch(self, request, pk):
        try:
            queryset = HouseManage.objects.get(pk=pk)
        except HouseManage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = HouseManageSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
