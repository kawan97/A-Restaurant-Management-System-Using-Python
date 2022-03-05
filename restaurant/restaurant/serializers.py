from django.contrib.auth.models import User
from rest_framework import serializers
from app.models import Profile,Item,SubItem,Order,OrderItem,Table,SubOrder

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields ='__all__'

class UserSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer(many=False,read_only=True)
    class Meta:
        model = User
        fields = [ 'username','profile']

class SubItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubItem
        fields ='__all__'

class ItemSerializer(serializers.ModelSerializer):
    subitem=SubItemSerializer(many=True,read_only=True)
    class Meta:
        model = Item
        fields = [ 'name','subitem']

class TablerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields ='__all__'


class SinglOrderIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id']

class SubOrderSerializer(serializers.ModelSerializer):
    User=UserSerializer(many=False,read_only=True)
    Table=TablerSerializer(many=False,read_only=True)
    Order=SinglOrderIdSerializer(many=False,read_only=True)
    class Meta:
        model = SubOrder
        fields = ['id','status','User','Table','Order']

class OrderSerializer(serializers.ModelSerializer):
    User=UserSerializer(many=False,read_only=True)
    Table=TablerSerializer(many=False,read_only=True)
    suborderorder=SubOrderSerializer(many=True,read_only=True)
    class Meta:
        model = Order
        fields = ['id','status','User','Table','suborderorder']




