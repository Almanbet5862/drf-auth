from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        UserModel = get_user_model()

        username, password = kwargs.get(UserModel.USERNAME_FIELD, None), kwargs.get('password', None)

        user = UserModel.objects.filter(username=username, is_active=True).first()
        if user and user.check_password(password):
            return user
        return None
