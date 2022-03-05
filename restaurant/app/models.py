from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    status=models.CharField(max_length=200,default='active')
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

class Table(models.Model):
    name = models.CharField(max_length=200)
    status=models.CharField(max_length=200,null=True, blank=True)
    def __str__(self):
        return self.name
class Order(models.Model):
    status=models.CharField(max_length=200,default='notpayed')
    date = models.DateTimeField(auto_now_add=True, blank=True)
    User=models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True, related_name='orderuser')
    Table=models.ForeignKey(Table,on_delete=models.CASCADE,null=True, blank=True, related_name='ordertable')
    def __str__(self):
        return 'orderid='+str(self.id)+' on table'+self.Table.name

class SubOrder(models.Model):
    status=models.CharField(max_length=200,default='ordering')
    date = models.DateTimeField(auto_now_add=True, blank=True)
    User=models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True, related_name='suborderuser')
    Table=models.ForeignKey(Table,on_delete=models.CASCADE,null=True, blank=True, related_name='subordertable')
    Order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True, blank=True, related_name='suborderorder')
    def __str__(self):
        return 'suborderid='+str(self.id)+' on table:'+self.Table.name+' in order:'+str(self.Order.id)

class OrderItem(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    User=models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True, related_name='orderitemuser')
    Table=models.ForeignKey(Table,on_delete=models.CASCADE,null=True, blank=True, related_name='orderitemtable')
    Order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True, blank=True, related_name='orderitemorder')
    SubOrder=models.ForeignKey(SubOrder,on_delete=models.CASCADE,null=True, blank=True, related_name='orderitemsuborder')
    SubItem=models.ForeignKey(SubItem,on_delete=models.CASCADE,null=True, blank=True, related_name='orderitemsubitem')

    def __str__(self):
        return 'OrderItem ='+str(self.id)+' suborder ='+str(self.SubOrder.id)+' SubItem:'+self.SubItem.name
    class Meta:
        ordering = ['SubOrder']

class Feedback(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    Order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True, blank=True, related_name='feedbackorder')
    status=models.CharField(max_length=200,default='notanswered')
    key=models.CharField(max_length=200)
    text = models.TextField(blank=True, null=True)
    def __str__(self):
        return 'OrderId ='+str(self.Order.id)
    class Meta:
        ordering = ['date']