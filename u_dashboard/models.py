from django.db import models
from django.contrib.auth.models import Group, ContentType, Permission
from django.contrib.postgres.fields.array import ArrayField
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.deletion import SET_NULL
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class Domain(models.Model):
    name = models.CharField(max_length=40, null=True, blank=True)
    subdomain = models.CharField(max_length=50, null=True, blank=True)

class DomainAware(models.Model):
   domain = models.ForeignKey("Domain", on_delete=models.CASCADE, null=True, blank=True)


class Member(DomainAware):
   name = models.CharField(max_length=40, null=True, blank=True)
