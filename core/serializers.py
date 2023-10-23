from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "password",
            "firstname",
            "lastname",
            "phone_number",
        )

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        user = User.objects.create_app_user(**validated_data)
        return user


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        options = {"hours": settings.TOKEN_LIFESPAN}
        refresh = self.get_token(self.user)
        access_token = refresh.access_token
        access_token.set_exp(lifetime=timedelta(**options))
        self.user.save_last_login()
        data['refresh'] = str(refresh)
        data['access'] = str(access_token)
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token.id = user.id
        token['firstname'] = user.firstname
        token['lastname'] = user.lastname
        token["username"] = user.username
        return token


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, required=False)
    new_password = serializers.CharField(max_length=128, min_length=5)

    def validate_old_password(self, value):
        request = self.context["request"]

        if not request.user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def save(self):
        user = self.context["request"].user
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save(update_fields=["password"])


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "firstname",
            "lastname",
            "created_at",
            "phone_number",
        ]

    def to_representation(self, instance):
        return super().to_representation(instance)


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "firstname",
            "lastname",
        ]

    def validate(self, attrs: dict):
        return super().validate(attrs)

    def update(self, instance, validated_data):
        if validated_data.get("password", False):
            validated_data.pop('password')
        instance = super().update(instance, validated_data)
        return instance


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "firstname",
            "lastname",
            "phone_number",
            "username",
            "password",
        )

        extra_kwargs = {
            "firstname": {"required": True},
            "lastname": {"required": True},
            "username": {"required": True},
            "password": {"required": True, "write_only": True},
        }

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return User.objects.create_app_user(**validated_data)
