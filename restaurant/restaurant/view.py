from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([IsAdminUser])
def GetUsers(requst):
    Users=User.objects.all()
    DataSerializer=UserSerializer(Users,many=True)
    print(DataSerializer.data)

    return Response(DataSerializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetRoutes(requst):
    Routes={
        'routes/':'see all possable routes',
        'users/':"get all users ",
        'admin/':"go to admin panel",

    }

    return Response(Routes,status=status.HTTP_200_OK)
