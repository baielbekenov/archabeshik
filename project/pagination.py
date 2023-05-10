from rest_framework.pagination import PageNumberPagination


class CommentPagination(PageNumberPagination):
    page_size = 14
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100


class ContentPagination(PageNumberPagination):
    page_size = 9
    page_query_param = 'page_size'
    max_page_size = 100


class HouseManagePagination(PageNumberPagination):
    page_size = 15
    page_query_param = 'page_size'
    max_page_size = 100