from django.contrib.auth import get_user
from rest_framework import serializers

from project.models import User, Category, Content, HouseManage, Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class HouseManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseManage
        fields = ['id', 'title', 'amount_of_rooms', 'phone_number', 'category_id', 'photoes',
                  'price', 'description' ]


    # def create(self):


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


# class ContentListSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Content
#         fields = ['id', 'title', 'image']



