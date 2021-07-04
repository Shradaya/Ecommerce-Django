from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=10, default=0)
    email = models.EmailField(null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.full_name




