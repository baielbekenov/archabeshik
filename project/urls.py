from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from project import views




urlpatterns = [
    path('register/', views.RegistrationAPIView.as_view(template_name='templates/registration.html')),
    path('login/', views.LoginAPIView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),
    path('category_create/', views.CategoryCreateAPIView.as_view()),
    path('category_list/', views.CategoryListAPIView.as_view()),
    path('content_detail/<int:pk>/', views.ContentDetail.as_view()),
    path('content_list/', views.ContentList.as_view()),
    path('content_create/', views.ContentCreate.as_view()),
    # path('renthouse_list/', views.RentHouseList.as_view()),
    # path('renthouse_detail/<int:pk>/', views.RentHouseDetail.as_view()),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('comment_list/', views.CommentListAPIView.as_view()),
    path('comment_delete/<int:id>/', views.CommentDestroyAPIView.as_view()),
    path('housemanage_create/', views.HouseManageCreateAPIView.as_view()),
    path('housemanage_list/', views.HouseManageListAPIView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)

