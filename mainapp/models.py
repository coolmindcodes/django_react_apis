from django.contrib.auth.models import AbstractUser
from django.db import models


class Permission(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        db_table='permissions'

class Role(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission)
    class Meta:
        db_table='roles'

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table='users'