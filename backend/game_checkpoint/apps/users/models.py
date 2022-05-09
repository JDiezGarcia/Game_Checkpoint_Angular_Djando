from uuid import uuid4
from django.db import models
from django.core.validators import MinLengthValidator, FileExtensionValidator
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from game_checkpoint.apps.core.models import TimestampedModel


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, username, email, password=None, role="user"):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model( username=username, email=self.normalize_email(email), role=role)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password, role):
      """
      Create and return a `User` with superuser powers.

      Superuser powers means that this use is an admin that can do anything
      they want.
      """
      if password is None:
          raise TypeError('Superusers must have a password.')

      user = self.create_user(username, email, password, 'SUPERADMIN')
      user.save()

      return user


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    ROLE_CHOICES = [
        ('USER', 'user'),
        ('ADMIN', 'admin'),
        ('SUPERADMIN', 'superadmin')
    ]
    uuid = models.UUIDField(primary_key=True ,unique=True, db_index=True, default=uuid4)
    username = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(choices=ROLE_CHOICES, default='USER', max_length=32)
    image = models.FileField(upload_to='img/users', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    respect = models.IntegerField(default=0)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']
    objects = UserManager()

    @property
    def is_staff(self):
        return self.role == 'ADMIN' or self.role == 'SUPERADMIN'

    @property
    def is_superuser(self):
        return self.role == 'SUPERADMIN'

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.follower) + ' ('+ str(self.id) +')'
