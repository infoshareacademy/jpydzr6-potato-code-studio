from django.contrib.auth.backends import BaseBackend
from store.models import UserProfile

class UserProfileAuthentication(BaseBackend):
    def authenticate(self, request, username = None , password = None):
        try:
            user = UserProfile.objects.get(username=username)
            if user.check_password(password):
                return user
            else:
                return None
            
        except UserProfile.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return UserProfile.objects.get(pk=user_id)
        except UserProfile.DoesNotExist:
            return None