from django.contrib import admin

from apis.models import User, Jobs, JobApplication

# Register your models here.
admin.site.register(User)
admin.site.register(Jobs)
admin.site.register(JobApplication)
