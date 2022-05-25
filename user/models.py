from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    class Meta:
        app_label = 'user'

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    size = models.SmallIntegerField(default=0)
    logo_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    class Meta:
        app_label = 'user'

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    avatar_url = models.URLField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    current_paper = models.ForeignKey('teacher.Paper', blank=True, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
