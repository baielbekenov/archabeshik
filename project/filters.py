from django_filters.rest_framework import FilterSet, CharFilter


class SearchFilterSet(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')