from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_email = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='user/images/%Y/%m/%d', null=True)
    sex = models.BooleanField(default=None, null=True)


    def __str__(self):
        return self.username


# Create your models here.
