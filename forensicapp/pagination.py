from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPaginationWithResult(PageNumberPagination):
    page_size = 8  # Default limit
    page_size_query_param = 'limit'
    max_page_size = 100  # Max allowed limit

    def get_paginated_response(self, data):
        return Response({
            "paginationResult": {
                "currentPage": self.page.number,
                "numberOfPages": self.page.paginator.num_pages,
                "limit": self.get_page_size(self.request)
            },
            "data": data
        })