from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer

@api_view(['GET'])
def GetUsers(requst):
    Users=User.objects.all()
    DataSerializer=UserSerializer(Users,many=True)
    print(DataSerializer.data)

    return Response(DataSerializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
def GetRoutes(requst):
    Routes={
        'routes/':'see all possable routes',
        'users/':"get all users ",
        'admin/':"go to admin panel",

    }

    return Response(Routes,status=status.HTTP_200_OK)