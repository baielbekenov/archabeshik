from django.contrib.auth import get_user
from rest_framework import serializers
from project.models import User, Category, Content, HouseManage, Comment, Report, Question, \
    Advertisement, History, HouseImage, ContentImage


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'is_superuser']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username already exists', code='409')
        return value

    def create(self, validated_data):
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email')
        user = User.objects.create(username=validated_data['username'],
                                   first_name=first_name,
                                   last_name=last_name, email=email)
        user.set_password(validated_data['password'])
        user.save()
        return user


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'is_rent']


class HouseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseImage
        fields = ('image',)


class HouseManageSerializer(serializers.ModelSerializer):
    photos = HouseImageSerializer(many=True, read_only=True)

    class Meta:
        model = HouseManage
        fields = '__all__'


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


class ContentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentImage
        fields = ('image',)


class ContentSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    photos = ContentImageSerializer(many=True, read_only=True)

    class Meta:
        model = Content
        fields = ['id', 'title', 'category_id', 'image', 'data_added', 'owner',
                  'content', 'comments', 'photos']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        else:
            return ''


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'


