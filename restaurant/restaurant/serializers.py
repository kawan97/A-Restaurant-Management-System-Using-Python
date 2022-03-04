from django.contrib.auth.models import User
from rest_framework import serializers
from app.models import Profile,Item,SubItem

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