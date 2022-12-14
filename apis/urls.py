from django.urls import path
from .views import (
    UserSignupViewSet,
    UserLoginViewSet,
    JobViewSet,
    UserJobViewSet,
    UserJobsApplicationViewSet,
)

urlpatterns = [
    # User APIs
    path("signup/", UserSignupViewSet.as_view({"post": "create"}), name="signup"),
    path("login/", UserLoginViewSet.as_view({"post": "create"}), name="login"),
    # Admin Job APIs
    path("admin_jobs/", JobViewSet.as_view({"post": "create"}), name="admin_jobs"),
    path(
        "admin_jobs_list/", JobViewSet.as_view({"get": "list"}), name="admin_jobs_list"
    ),
    path("update_job/", JobViewSet.as_view({"put": "update"}), name="update_job"),
    # User Job APIs
    path(
        "user_jobs_list/",
        UserJobViewSet.as_view({"get": "list"}),
        name="user_jobs_list",
    ),
    # User Job Application
    path(
        "apply_job/",
        UserJobsApplicationViewSet.as_view({"post": "create"}),
        name="apply_job",
    ),
    path(
        "user_job_applications/",
        UserJobsApplicationViewSet.as_view({"get": "list"}),
        name="user_job_applications",
    ),
    # Admin Job Application List
    path(
        "admin_job_applications/",
        UserJobsApplicationViewSet.as_view({"get": "list"}),
        name="admin_job_applications",
    ),
]
