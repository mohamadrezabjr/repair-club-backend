import re
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import validate_integer
from auth_app.managers import UserManager

def valid_phone_ir(value):
    pattern = r'^09\d{9}$'
    if not re.match(pattern , value) or len(value) != 11:
        raise ValidationError("phone number is not valid")
    return value

class User(AbstractUser):
    username = None
    email = None
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    phone = models.CharField(max_length=11, validators=[valid_phone_ir, validate_integer], unique=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone or self.get_username()

    def has_perm(self, perm, obj=None):
        return self.is_superuser or perm in self.get_all_permissions()

    def has_module_perms(self, app_label):
        return self.is_superuser or super().has_module_perms(app_label)