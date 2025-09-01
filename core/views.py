from rest_framework.viewsets import ModelViewSet
from core import serializers as CoreSerializers
from core import models as CoreModels
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status


# region Users APIs
class UserViewset(ModelViewSet):
    serializer_class = CoreSerializers.UsersSerializer
    queryset = CoreModels.Users.objects.filter(Q(
        status=CoreModels.Users.Status.ACTIVE
    ))

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.status = CoreModels.Users.Status.DELETED
        obj.save()
        return Response(
            data=CoreSerializers.UsersSerializer(obj).data,
            status=status.HTTP_200_OK
        )
# endregion

