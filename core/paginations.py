from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request


class DynamicPagination(PageNumberPagination):
    """
    a class that you can have custom pagination by limit in queryparams
    """
    page_size = 10

    def get_page_size(self, request: Request):
        if request.query_params.get('limit'):
            limit = request.query_params.get('limit')
            if limit.lower() == 'none':
                return False
            return limit
        return super().get_page_size(request)
