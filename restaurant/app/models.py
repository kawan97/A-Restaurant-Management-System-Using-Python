from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user_role = models.CharField(max_length=200)
    User=models.OneToOneField(User,on_delete=models.CASCADE)
    user_salary=models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
        return self.User.username
    class Meta:
        ordering = ['date']


