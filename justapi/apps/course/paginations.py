

from rest_framework.pagination import  PageNumberPagination as DRFPageNumberPagination

class PageNumberPagination(DRFPageNumberPagination):
    page_size=1
    page_query_param = 'page'
    max_page_size = 20
    page_size_query_param='page_size'


class PopularPageNumberPagination(DRFPageNumberPagination):
    page_size=30
    page_query_param = 'page'
    max_page_size = 30
    page_size_query_param='page_size'