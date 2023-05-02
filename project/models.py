from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


class User(AbstractUser):

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=80, verbose_name='Название')

    def __str__(self):
        return self.name


class Content(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='Категория', null=True)
    image = models.ImageField(verbose_name='Изображения')
    data_added = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name='contents', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title


class HouseManage(models.Model):
    title = models.CharField(max_length=100)
    amount_of_rooms = models.IntegerField(verbose_name='Количество комнат')
    phone_number = models.IntegerField(verbose_name='Номер телефона')
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='Категория', null=True)
    photoes = models.ImageField(verbose_name='Картинки')
    price = models.IntegerField(verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=60, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    comment = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name





