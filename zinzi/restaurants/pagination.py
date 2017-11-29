from rest_framework.pagination import PageNumberPagination


class RestaurantListPagination(PageNumberPagination):
    # fixme - 일단 page_size가 정해지지 않아 10개로 작성
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000
