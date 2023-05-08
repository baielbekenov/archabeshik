from django.contrib.auth import get_user, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from project.models import User, Category, Content, HouseManage, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'is_rent']


class HouseManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseManage
        fields = ['id', 'title', 'owner',  'amount_of_rooms', 'phone_number', 'category_id', 'remont', 'photos',
                 'udobstva', 'price', 'description' ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'email', 'comment', 'pub_date']

    # def create(self, validated_data):
    #     user = get_user(self.context['request'])
    #     if user.is_authenticated:
    #         self.fields['name'].read_only = True
    #         self.fields['email'].read_only = True
    #         validated_data['name'] = user.username
    #         validated_data['email'] = user.email
    #     return super().create(validated_data)


class ContentSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Content
        fields = ['id', 'title', 'category_id', 'image', 'data_added', 'owner', 'content', 'comments']

    def get_image(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'name']




