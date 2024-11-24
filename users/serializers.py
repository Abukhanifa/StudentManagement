from djoser.serializers import UserSerializer
from .models import CustomUser

class UserViewSerializer(UserSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']
        
    def create(self, validated_data):
    # Create the user with the role
        user = CustomUser.objects.create_user(**validated_data)
        # The signal will automatically create the student instance if role is 'Student'
        return user