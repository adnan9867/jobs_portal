from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

from apis.custom_manager import UserManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


USER_ROLE_CHOICES = (
    ("Admin", "Admin"),
    ("Job_Hunter", "Job_Hunter"),
)


class User(BaseModel, AbstractUser):
    role = models.CharField(
        max_length=20, choices=USER_ROLE_CHOICES, default="Job_Hunter"
    )
    email = models.EmailField(unique=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Jobs(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    occupied = models.BooleanField(default=False)


class JobApplication(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_in_job_application"
    )
    job = models.ForeignKey(
        Jobs, on_delete=models.CASCADE, related_name="job_in_job_application"
    )
    resume = models.FileField(
        upload_to="resume", validators=[FileExtensionValidator(["pdf", "doc", "docx"])]
    )
