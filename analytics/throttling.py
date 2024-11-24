from rest_framework.throttling import UserRateThrottle
from analytics.models import ApiRequest

class RequestTrackerThrottle(UserRateThrottle):
    def allow_request(self, request, view):
        if super().allow_request(request, view):
            ApiRequest.objects.create(user=request.user, endpoint=request.path)
            return True
        return False
