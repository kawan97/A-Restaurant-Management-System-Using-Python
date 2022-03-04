from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer

# login and acces token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        refresh['username']=self.user.username
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['username'] = self.user.username
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# get all users
@api_view(['GET'])
@permission_classes([IsAdminUser])
def GetUsers(requst):
    Users=User.objects.all()
    DataSerializer=UserSerializer(Users,many=True)
    print(requst.user.profile.date)

    return Response(DataSerializer.data,status=status.HTTP_200_OK)

# all routes
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetRoutes(requst):
    Routes={
        '':'welcome',
        'api/routes/':'see all possable routes',
        'api/users/':"get all users ",
        'admin/':"go to admin panel",

    }

    return Response(Routes,status=status.HTTP_200_OK)


# home
@api_view(['GET'])
def GetHome(requst):
    msg={
        'home':'welcome to home',
    }

    return Response(msg,status=status.HTTP_200_OK)
