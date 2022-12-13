from rest_framework import serializers
from apis.models import User, Jobs, JobApplication
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken


class UserSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "password", "username")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializers(serializers.Serializer):  # noqa
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        max_length=128,
        write_only=True,
    )

    def validate(self, data):
        username = data.get("email")
        password = data.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")
        refresh = RefreshToken.for_user(user)
        data = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": user.id,
        }
        return data


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "username"]


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = "__all__"


class UserJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = ["id", "title", "description", "location"]


class JobApplicationSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)

    class Meta:
        model = JobApplication
        fields = "__all__"
