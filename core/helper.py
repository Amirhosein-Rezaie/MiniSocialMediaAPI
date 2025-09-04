from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer
from rest_framework import status
from django.db.models import Choices
from django.db.models import Model
from django.db.models import (ForeignKey, OneToOneField, ManyToManyField)
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import FieldDoesNotExist, FieldError


def update_status_value(request: Request, self, status_class: Choices, seriaizer: ModelSerializer):
    """
    A function for update status field and validate it.
    """
    instance = self.get_object()
    status_value = request.data.get('status')

    if status_value is None:
        return Response({"detail": "status is required"}, status=status.HTTP_400_BAD_REQUEST,)
    if status_value not in list(status_class):
        return Response({"detail": "status value is not valid.", }, status=status.HTTP_400_BAD_REQUEST)

    instance.status = status_value
    instance.save(update_fields=['status'])
    return Response(seriaizer(instance).data, status=status.HTTP_200_OK)


# set limit of paginators in class and function base views
def limit_paginate(request: Request, pagination_class: PageNumberPagination):
    """
    get limit from query params and return.
    """
    if request.query_params.get('limit'):
        return request.query_params.get('limit')
    return pagination_class.page_size


# functions
def dynamic_search(self, request: Request, model: Model):
    """
    a function that you can have dynamic search.
    """
    # variables
    like = "istartswith"
    out_query_params = ['limit', 'page']
    paginator = self.pagination_class
    serializer = self.serializer_class
    equal_to_fields = ['id']

    query_params = request.query_params
    if query_params:
        query_search = Q()

        for key, value in query_params.items():
            if key in out_query_params:
                continue

            if not value:
                return Response(
                    {"detail": "value for search is empty."},
                    status=status.HTTP_400_BAD_REQUEST)

            search_items = key.split('-')
            field_name = search_items[0]

            try:
                field_obj = model._meta.get_field(field_name)

                if isinstance(field_obj, (ForeignKey, ManyToManyField, OneToOneField)):
                    try:
                        sub_field_name = search_items[1]
                        if sub_field_name.lower() not in equal_to_fields:
                            query_search &= Q(
                                **{f"{field_name}__{sub_field_name}__{like}": value}
                            )
                        else:
                            query_search &= Q(
                                **{f"{field_name}__{sub_field_name}": value}
                            )
                    except IndexError:
                        return Response(
                            {"detail": "Set second field for foreign fields."},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    if field_name.lower() not in equal_to_fields:
                        query_search &= Q(
                            **{f"{field_name}__{like}": value}
                        )
                    else:
                        query_search &= Q(
                            **{f"{field_name}": value}
                        )
            except (FieldDoesNotExist, FieldError):
                return Response(
                    data={
                        "detail": "Not found field.",
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        founds = model.objects.filter(query_search)

        if paginator:
            limit_paginate(request=request, pagination_class=paginator)
            paginated_founds = paginator.paginate_queryset(founds, request)
            serialize_found = serializer(paginated_founds, many=True)
            return paginator.get_paginated_response(serialize_found.data)
        else:
            return Response(
                serializer(founds, many=True).data,
                status=status.HTTP_200_OK
            )
