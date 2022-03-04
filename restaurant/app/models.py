from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user_role = models.CharField(max_length=200)
    User=models.OneToOneField(User,on_delete=models.CASCADE,null=True, blank=True, related_name='profile')
    user_salary=models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
        return self.User.username
    class Meta:
        ordering = ['date']

class Item(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class SubItem(models.Model):
    name = models.CharField(max_length=200)
    Item=models.ForeignKey(Item,on_delete=models.CASCADE,null=True, blank=True, related_name='subitem')
    item_price=models.CharField(max_length=64)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['Item']