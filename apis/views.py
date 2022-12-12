from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .contants import *
from apis.models import User
from apis.serializers import UserSignupSerializer, LoginSerializers


class UserSignupViewSet(ModelViewSet):
    """
    Create a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({SUCCESS: True,
                             STATUS_CODE: status.HTTP_201_CREATED,
                             MESSAGE: "User created successfully"
                             },
                            status=status.HTTP_201_CREATED,
                            headers=headers
                            )
        except Exception as e:
            return Response({SUCCESS: False, ERROR: str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginViewSet(ModelViewSet):
    """
    Login a user with a given email and password.
    """
    queryset = User.objects.all()
    serializer_class = LoginSerializers

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response({SUCCESS: True,
                             STATUS_CODE: status.HTTP_200_OK,
                             MESSAGE: "User login successfully",
                             DATA: serializer.data
                             },
                            status=status.HTTP_200_OK,
                            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e)},
                status=status.HTTP_400_BAD_REQUEST
                            )
