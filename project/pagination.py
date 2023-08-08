from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CommentPagination(PageNumberPagination):
    page_size = 14
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # общее количество элементов
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


class CategoryPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100


class ContentPagination(PageNumberPagination):
    page_size = 12
    page_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # общее количество элементов
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


class HouseManagePagination(PageNumberPagination):
    page_size = 15
    page_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # общее количество элементов
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


class ReportPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class QuestionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class AdvertisementPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100


class HistoryPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100