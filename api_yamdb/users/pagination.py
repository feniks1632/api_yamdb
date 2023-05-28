from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10  # количество элементов на странице
    page_size_query_param = 'page_size'  # позволяет клиенту задавать количество элементов на странице
    max_page_size = 100  # максимальное количество элементов на странице
    
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # включить ключ "count" в ответ
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })