from rest_framework.pagination import PageNumberPagination
from django.db.models import QuerySet, Q
import logging

class GlobalPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200


def filter_and_order(queryset: QuerySet, request):
    excluded_params = ['page', 'page_size', 'order_by']
    # Apply filtering based on request query parameters
    logging.debug(f"Request GET parameters: {request.GET}")
    
    filter_params = Q()
    for key, value in request.GET.items():
        if key not in excluded_params:
            if key.endswith('id'):
                lookup_key = key  # For ID lookups, no change
            elif '__' in key:
                # For ForeignKey fields, use icontains for string fields
                if 'username' in key or 'name' in key:  # Adjust according to your related model fields
                    lookup_key = f"{key}__icontains"
                else:
                    lookup_key = key  # Keep it as is if not a string field
            else:
                lookup_key = f"{key}__icontains"  # General case for non-foreign fields

            # Add to the filter params
            filter_params &= Q(**{lookup_key: value})

    # Apply filtering
    queryset = queryset.filter(filter_params)
    
    logging.debug(f"Final queryset: {queryset.query}")
    logging.debug(f"Filter parameters: {filter_params}")


    # Apply ordering if 'order_by' is present in query parameters
    order_by_param = request.GET.get('order_by')
    if order_by_param:
        queryset = queryset.order_by(order_by_param)

    return queryset
