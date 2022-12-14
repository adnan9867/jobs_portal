from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .contants import *
from apis.models import User, Jobs, JobApplication
from apis.serializers import (
    UserSignupSerializer,
    LoginSerializers,
    JobSerializer,
    JobApplicationSerializer,
    UserJobSerializer, JobApplicationSerializerNew,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class UserSignupViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new user.
        """
        try:
            data = request.data
            user = User.objects.filter(email=data["email"]).first()
            if user:
                return Response(
                    {ERROR: "User already exists", SUCCESS: False},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {
                    SUCCESS: True,
                    STATUS_CODE: status.HTTP_201_CREATED,
                    MESSAGE: "User created successfully",
                },
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e.args[0])},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserLoginViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializers

    def create(self, request, *args, **kwargs):
        """
        Login a user with a given email and password.
        """
        try:
            data = request.data
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            return Response(
                {
                    SUCCESS: True,
                    STATUS_CODE: status.HTTP_200_OK,
                    MESSAGE: "User login successfully",
                    DATA: serializer.validated_data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e.args[0])},
                status=status.HTTP_400_BAD_REQUEST,
            )


class JobViewSet(ModelViewSet):
    queryset = Jobs.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        """
        Create a new job.
        """
        try:
            data = request.data
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {
                    SUCCESS: True,
                    STATUS_CODE: status.HTTP_201_CREATED,
                    MESSAGE: "Job created successfully",
                    DATA: serializer.data,
                },
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    def list(self, request, *args, **kwargs):
        """
        List all jobs for admin.
        """
        try:
            queryset = self.filter_queryset(self.get_queryset().order_by("-id"))
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {
                    SUCCESS: True,
                    STATUS_CODE: status.HTTP_200_OK,
                    MESSAGE: "Job list",
                    DATA: serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        """
        Update a job.
        """
        try:
            data = request.data
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {
                    SUCCESS: True,
                    STATUS_CODE: status.HTTP_200_OK,
                    MESSAGE: "Job updated successfully",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class UserJobViewSet(ModelViewSet):
    queryset = Jobs.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        List all jobs for a user.
        """
        try:
            job_title = request.query_params.get("job_title", None)
            location = request.query_params.get("location", None)
            queryset = self.filter_queryset(
                self.get_queryset().filter(occupied=False).order_by("-id")
            )
            if job_title is not None:
                queryset = queryset.filter(title__icontains=job_title)
            if location is not None:
                queryset = queryset.filter(location__icontains=location)
            serializer = UserJobSerializer(queryset, many=True)
            return Response(
                {
                    SUCCESS: True,
                    STATUS_CODE: status.HTTP_200_OK,
                    MESSAGE: "Job list",
                    DATA: serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class UserJobsApplicationViewSet(ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        List all jobs applied by a user.
        """
        try:
            user = request.user
            queryset = self.queryset.filter(user=user).order_by("-id")
            serializer = JobApplicationSerializer(queryset, many=True)
            return Response(
                {
                    SUCCESS: True,
                    STATUS_CODE: status.HTTP_200_OK,
                    MESSAGE: "User job application list",
                    DATA: serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request, *args, **kwargs):
        """
        Apply for a job.
        """
        try:
            data = request.data
            data["user"] = request.user.id
            previous_application = self.queryset.filter(
                user=request.user, job=data["job"]
            )
            if previous_application.exists():
                return Response(
                    {
                        SUCCESS: False,
                        ERROR: "You have already applied for this job",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = JobApplicationSerializerNew(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    SUCCESS: True,
                    STATUS_CODE: status.HTTP_200_OK,
                    MESSAGE: "Job applied successfully",
                    DATA: serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class AdminJobApplicationViewSet(ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        """
        List all jobs applied by a user.
        """
        try:
            queryset = self.queryset.all().order_by("-id")
            serializer = self.serializer_class(queryset, many=True)
            return Response(
                {
                    SUCCESS: True,
                    STATUS_CODE: status.HTTP_200_OK,
                    DATA: serializer.data,
                    MESSAGE: "Job application list",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
