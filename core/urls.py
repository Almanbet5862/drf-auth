from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from core.views import *

app_name = "drf-custom-auth"
router = DefaultRouter()

router.register("auth/registration", RegistrationView, basename="registration")
router.register("auth/change-password", PasswordChangeView, basename="password-change")
router.register("user", UserViewSets, basename="user")

urlpatterns = [
    path("auth/login/", LoginTokenPairView.as_view(), name="login"),
    # path("auth/token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    # path("auth/token/verify/", TokenVerifyView.as_view(), name="verify-token"),
    path("", include(router.urls)),
]
