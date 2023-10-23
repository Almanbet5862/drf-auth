from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .filters import UserFilter
from .permissions import IsAdmin, is_admin_user
from .serializers import *


class RegistrationView(viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        context = {"request": request}
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)


class LoginTokenPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer


class PasswordChangeView(viewsets.GenericViewSet):
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        context = {"request": request}
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Ваш пароль был изменен"}, status.HTTP_200_OK)


class UserViewSets(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = ListUserSerializer
    permission_classes = [IsAdmin]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = UserFilter  # custom filter user in filters.py
    search_fields = ["username", "firstname", "lastname", "phone"]
    ordering_fields = [
        "username",
        "firstname",
        "lastname",
        "phone",
        "created_at",
    ]

    def get_queryset(self):
        user = self.request.user
        if is_admin_user(user):
            return super().get_queryset().all()
        return super().get_queryset().filter(id=user.id)

    def get_serializer_class(self):
        if self.action in ["create"]:
            return CreateUserSerializer
        if self.action in ["update"]:
            return UpdateUserSerializer
        return super().get_serializer_class()

    @extend_schema(responses={200: ListUserSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(responses={200: CreateUserSerializer()})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
