from django.contrib.auth.models import User
from rest_framework import serializers
from app.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields ='__all__'

class UserSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer(many=False,read_only=True)
    class Meta:
        model = User
        fields = [ 'username','profile']

