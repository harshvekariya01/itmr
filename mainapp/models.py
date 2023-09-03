from django.db import models
from django.contrib.auth.models import User
# Create your models here.

department = (
    ('1','Leadership'),
    ('2','Executive'),
)
class userType(models.Model):
    user = models.OneToOneField(User, on_delete = models.SET_NULL, null = True)
    userdepartment = models.CharField(max_length=1, choices=department, default=2)


class URLDetail(models.Model):

    status = models.CharField(max_length=10, null=False)
    project_id = models.CharField(max_length=100, null=False)
    unique_id = models.CharField(max_length=100, null=False)
    ip_address = models.CharField(max_length=15, null=False)
    country = models.CharField(max_length=50, null=True)
    regionName = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=100, null=True)
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)

    class Meta:
        ordering  = ('-id',)
    
    def __str__(self):
        return "Project ID: " + self.project_id +"-- Unique ID: " + self.unique_id