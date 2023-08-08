from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from project import views

urlpatterns = [
    path('register/', views.RegistrationAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),
    path('category_create/', views.CategoryCreateAPIView.as_view()),
    path('category_list/', views.CategoryListAPIView.as_view()),
    path('content_detail/<int:pk>/', views.ContentDetail.as_view()),
    path('content_list/', views.ContentList.as_view()),
    path('content_list/<int:category>/', views.Contentlist.as_view()),
    path('content_create/', views.ContentCreate.as_view()),
    path('content_delete/<int:pk>/', views.ContentDelete.as_view()),
    path('content_update/<int:pk>/', views.ContentPatchView.as_view()),
    path('content_search/', views.ContentSearchAPIView.as_view()),
    path('comment_list/<int:content_id>/', views.CommentListAPIView.as_view()),
    path('housemanage_create/', views.HouseManageCreateAPIView.as_view()),
    path('content_list/housemanage/', views.HouseManageListAPIView.as_view()),
    path('housemanage_list/<int:pk>/', views.HouseManageRetrive.as_view()),

    path('create_advert/', views.AdvertisementCreateAPIView.as_view()),

    path('report_list/', views.ReportAPIView.as_view()),
    path('question_list/', views.QuestionAPIView.as_view()),
    path('advert_list/', views.AdvertisementListAPIView.as_view()),
    path('history_list/', views.HistoryListAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
