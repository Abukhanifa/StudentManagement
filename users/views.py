from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import CustomUser
from .serializers import UserViewSerializer
import logging
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

logger = logging.getLogger('app_logger')


class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserViewSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of users (Admin only)",
        responses={200: UserViewSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve details of a specific user",
        responses={200: UserViewSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an existing user record",
        request_body=UserViewSerializer,
        responses={200: UserViewSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a user record",
        responses={204: 'No Content'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Assign a role to a user (Admin only)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'role': openapi.Schema(type=openapi.TYPE_STRING, description='Role to assign to the user')
            }
        ),
        responses={200: UserViewSerializer}
    )
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsAdminUser])
    def assign_role(self, request, pk=None):
        user = CustomUser.objects.get(pk=pk)
        role = request.data.get('role')
        if role and role in dict(CustomUser.ROLE_CHOICES).keys():
            user.role = role
            user.save()
            return Response(UserViewSerializer(user).data, status=status.HTTP_200_OK)
