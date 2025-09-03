from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer
from rest_framework import status
from django.db.models import Choices


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
