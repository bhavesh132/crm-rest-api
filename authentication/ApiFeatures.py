from rest_framework.pagination import PageNumberPagination
from django.db.models import QuerySet, Q
import logging

class GlobalPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200


def filter_and_order(queryset: QuerySet, request):
    excluded_params = ['page', 'page_size', 'order_by']
    logging.debug(f"Request GET parameters: {request.GET}")

    filter_params = Q()

    # Use request.GET.lists() to capture all values for each parameter
    for key, values in request.GET.lists():
        if key not in excluded_params:
            if len(values) > 1:  # If there are multiple values for a field
                if key.endswith('id'):
                    lookup_key = key  # For ID lookups
                elif '__' in key:
                    if 'username' in key or 'name' in key:  # Adjust for ForeignKey string fields
                        lookup_key = f"{key}__in"
                    else:
                        lookup_key = key  # Keep as is for non-string ForeignKey fields
                else:
                    lookup_key = f"{key}__in"  # Use __in for non-foreign fields

                # Apply __in filter for multiple values
                filter_params &= Q(**{lookup_key: values})
            else:
                # Single value case, fall back to icontains where appropriate
                single_value = values[0]
                if key.endswith('id'):
                    lookup_key = key
                elif '__' in key:
                    if 'username' in key or 'name' in key:
                        lookup_key = f"{key}__icontains"
                    else:
                        lookup_key = key
                else:
                    lookup_key = f"{key}__icontains"

                filter_params &= Q(**{lookup_key: single_value})

    # Apply filtering
    queryset = queryset.filter(filter_params)
    logging.debug(f"Final queryset: {queryset.query}")
    logging.debug(f"Filter parameters: {filter_params}")

    # Apply ordering if 'order_by' is present in query parameters
    order_by_param = request.GET.get('order_by')
    if order_by_param:
        queryset = queryset.order_by(order_by_param)

    return queryset
