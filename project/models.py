from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=80, verbose_name='Название')
    is_rent = models.BooleanField(blank=True, null=True, default=True)

    def __str__(self):
        return self.name


class Content(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='Категория', null=True)
    image = models.ImageField(verbose_name='Изображения')
    data_added = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name='contents', on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title


class ContentImage(models.Model):
    content = models.ForeignKey('Content', on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='content_photos/')


class HouseManage(models.Model):
    title = models.CharField(max_length=100)
    owner = models.CharField(max_length=100, verbose_name='Владелец', blank=True, null=True)
    amount_of_rooms = models.IntegerField(verbose_name='Количество комнат', blank=True, null=True)
    phone_number = models.IntegerField(verbose_name='Номер телефона')
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='Категория', null=True)
    remont = models.CharField(max_length=50, verbose_name='Ремонт', blank=True, null=True)
    udobstva = models.CharField(max_length=300, verbose_name='Удобства', blank=True, null=True)
    photoss = models.ImageField(verbose_name='Картинки')
    price = models.IntegerField(verbose_name='Цена')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']


class HouseImage(models.Model):
    house = models.ForeignKey('HouseManage', on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='houses/')


class Comment(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=60, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    comment = models.TextField(verbose_name='Текст')
    pub_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии'

    def __str__(self):
        return self.name


class Report(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя')
    phone_number = models.CharField(max_length=10, verbose_name='Номер телефона', blank=True, null=True)
    text = models.TextField(verbose_name='Текст')

    def __str__(self):
        return self.name


class Question(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя')
    phone_number = models.CharField(max_length=10, verbose_name='Номер телефона', blank=True, null=True)
    text = models.TextField(verbose_name='Текст')

    def __str__(self):
        return self.name


class Advertisement(models.Model):
    image = models.ImageField(verbose_name='Изображения', blank=True, null=True)
    title = models.CharField(max_length=250, verbose_name='Название рекламы', blank=True, null=True)
    text = models.CharField(max_length=500, verbose_name='Текст')
    phone_number = models.CharField(max_length=10, verbose_name='Номер телефона', blank=True, null=True)
    link = models.URLField(max_length=200, verbose_name='Ссылка')

    def __str__(self):
        return self.title


class History(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название истории')
    image = models.ImageField(upload_to='images/history', verbose_name='Изображения', blank=True, null=True)
    text = models.TextField()

    def __str__(self):
        return self.title
