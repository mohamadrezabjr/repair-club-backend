from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def _create_user(self, phone, password, **kwargs):
        user = self.model(phone=phone, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(phone, password, **kwargs)

    def create_superuser(self, phone, password, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)

        if kwargs.get('is_superuser') is not True:
            raise ValueError("superuser must have is_superuser=True")
        if kwargs.get('is_staff') is not True:
            raise ValueError("superuser must have is_staff=True")

        return self._create_user(phone, password, **kwargs)