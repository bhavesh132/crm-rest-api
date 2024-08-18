from rest_framework.pagination import PageNumberPagination
from django.db.models import QuerySet, Q

class GlobalPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


def filter_and_order(queryset: QuerySet, request):
    excluded_params = ['page', 'page_size', 'order_by']
    # Apply filtering based on request query parameters
    filter_params = Q()
    for key, value in request.GET.items():
        if key not in excluded_params:
            # Modify the key to use __iexact or __icontains
            lookup_key = f"{key}__icontains"  # or use __iexact for exact case-insensitive match
            filter_params &= Q(**{lookup_key: value})

    # Apply filtering
    queryset = queryset.filter(filter_params)
    
    # Apply ordering if 'order_by' is present in query parameters
    order_by_param = request.GET.get('order_by')
    if order_by_param:
        queryset = queryset.order_by(order_by_param)

    return queryset
