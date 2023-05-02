from django.contrib import admin

from project.models import User, Category, Content, HouseManage, Comment

# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Content)
admin.site.register(HouseManage)
admin.site.register(Comment)