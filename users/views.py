import logging
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from .models import CustomUser
from .serializers import UserSerializer

# Set up logger
logger = logging.getLogger('user_actions')

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Ensure only admins can modify roles

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def assign_role(self, request, pk=None):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            logger.error(f"Failed to assign role: User with ID {pk} not found")
            return Response({'error': 'User not found'}, status=404)

        role = request.data.get('role')
        if role in dict(CustomUser.ROLE_CHOICES).keys():
            user.role = role
            user.save()
            logger.info(f"Assigned role '{role}' to user {user.username} (ID: {user.id})")
            return Response(UserSerializer(user).data)
        
        logger.warning(f"Invalid role '{role}' attempted for user ID {pk}")
        return Response({'error': 'Invalid role.'}, status=400)
