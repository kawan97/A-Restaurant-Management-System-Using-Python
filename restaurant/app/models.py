from django.db import models
from django.contrib.auth.models import User
# Create your models here.

PROFILE_STATUS_CHOICES = (
    ('active','active'),
    ('deactivate', 'deactivate'),
)
PROFILE_ROLE_CHOICES = (
    ('admin','admin'),
    ('chef', 'chef'),
    ('captain', 'captain'),
    ('waiter', 'waiter'),
)
class Profile(models.Model):
    status=models.CharField(max_length=200,choices=PROFILE_STATUS_CHOICES,default='active')
    user_role = models.CharField(max_length=200,choices=PROFILE_ROLE_CHOICES,null=False, blank=False)
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


TABLE_STATUS_CHOICES = (
    ('empty','empty'),
    ('reserved', 'reserved'),
)
class Table(models.Model):
    name = models.CharField(max_length=200)
    status=models.CharField(max_length=200,null=True, blank=True,choices=TABLE_STATUS_CHOICES)
    def __str__(self):
        return self.name


ORDER_STATUS_CHOICES = (
    ('payed','payed'),
    ('notpayed', 'notpayed'),
)
class Order(models.Model):
    status=models.CharField(max_length=200,default='notpayed',choices=ORDER_STATUS_CHOICES)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    User=models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True, related_name='orderuser')
    Table=models.ForeignKey(Table,on_delete=models.CASCADE,null=True, blank=True, related_name='ordertable')
    def __str__(self):
        return 'orderid='+str(self.id)+' on table'+self.Table.name

SUBORDER_STATUS_CHOICES = (
    ('ordering','ordering'),
    ('sendingtochef', 'sendingtochef'),
    ('chefaccepting', 'chefaccepting'),
    ('orderisready', 'orderisready'),
    ('waiteraccept', 'waiteraccept'),
    ('waiterserving', 'waiterserving'),
    ('suborderclosed', 'suborderclosed'),
)
class SubOrder(models.Model):
    status=models.CharField(max_length=200,default='ordering',choices=SUBORDER_STATUS_CHOICES)
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


FEEDBACK_STATUS_CHOICES = (
    ('notanswered','notanswered'),
    ('answered', 'answered'),
)
class Feedback(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    Order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True, blank=True, related_name='feedbackorder')
    status=models.CharField(max_length=200,default='notanswered',choices=FEEDBACK_STATUS_CHOICES)
    key=models.CharField(max_length=200)
    text = models.TextField(blank=True, null=True)
    def __str__(self):
        return 'OrderId ='+str(self.Order.id)
    class Meta:
        ordering = ['date']

ACTION_TYPE_CHOICES = (
    ('ordering','ordering'),
    ('sendingtochef', 'sendingtochef'),
    ('chefaccepting', 'chefaccepting'),
    ('orderisready', 'orderisready'),
    ('waiteraccept', 'waiteraccept'),
    ('waiterserving', 'waiterserving'),
    ('suborderclosed', 'suborderclosed'),
)
class Action(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    SubOrder=models.ForeignKey(SubOrder,on_delete=models.CASCADE,null=True, blank=True, related_name='actionsuborder')
    User=models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True, related_name='actionuser')
    type=models.CharField(max_length=200,null=False, blank=False,choices=ACTION_TYPE_CHOICES)
    def __str__(self):
        return 'SubOrder ='+str(self.SubOrder.id)+' ,type='+self.type
    class Meta:
        ordering = ['date']

class Payment(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    Order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True, blank=True, related_name='paymentorder')
    User=models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True, related_name='paymentuser')
    total=models.CharField(max_length=200,null=False, blank=False)
    def __str__(self):
        return 'payment ='+str(self.id)+' ,orderid='+str(self.Order.id)
    class Meta:
        ordering = ['date']

class Payment(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    Order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True, blank=True, related_name='paymentorder')
    User=models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True, related_name='paymentuser')
    total=models.CharField(max_length=200,null=False, blank=False)
    def __str__(self):
        return 'payment ='+str(self.id)+' ,orderid='+str(self.Order.id)
    class Meta:
        ordering = ['date']

class Equipment(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    User=models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True, related_name='equipmentuser')
    total=models.CharField(max_length=200,null=False, blank=False)
    name = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'name='+self.User.username+' ,equipment id='+str(self.id)
    class Meta:
        ordering = ['date']