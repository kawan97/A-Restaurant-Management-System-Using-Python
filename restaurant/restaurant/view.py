from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import ItemSerializer, UserSerializer,OrderSerializer,SubOrderSerializer
from app.models import Item,Order,SubOrder

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

# get all Items
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetItems(requst):
    try:
        items=Item.objects.all()
        DataSerializer=ItemSerializer(items,many=True)
        # print(requst.user.profile.date)
        return Response(DataSerializer.data,status=status.HTTP_200_OK)
    except:
         return Response({'detail':'sorry we havent any item'},status=status.HTTP_204_NO_CONTENT)
  

# get one Items
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetItem(requst,pk):
    try:
        items=Item.objects.get(id=pk)
        DataSerializer=ItemSerializer(items,many=False)
        # print(requst.user.profile.date)
        return Response(DataSerializer.data,status=status.HTTP_200_OK)
    except:
         return Response({'detail':'sorry we havent any item'},status=status.HTTP_204_NO_CONTENT)

# get orders
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetOrders(requst):
    try:
        orders=Order.objects.filter(status='notpayed').prefetch_related('suborderorder')
        # orders=orders.filter(suborderorder__status='ordering')
        # .filter(suborderorder__status='ordering')
        print(orders)
        DataSerializer=OrderSerializer(orders,many=True)
        return Response(DataSerializer.data,status=status.HTTP_200_OK)
    except:
        return Response({'detail':'sorry we havent any order'},status=status.HTTP_204_NO_CONTENT)
 # get single order
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetOrder(requst,pk):
    try:
        orders=Order.objects.filter(id=int(pk)).prefetch_related('suborderorder')
        # orders=orders.filter(suborderorder__status='ordering')
        # .filter(suborderorder__status='ordering')
        # print(orders)
        DataSerializer=OrderSerializer(orders,many=True)
        if(len(DataSerializer.data)==1):
            return Response(DataSerializer.data,status=status.HTTP_200_OK)
        else:
            return Response({'detail':f'sorry we havent  order {pk}'},status=status.HTTP_204_NO_CONTENT)

    except:
        return Response({'detail':f'sorry we havent  order {pk}'},status=status.HTTP_204_NO_CONTENT)
  # get single Sub Order
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetSubOrder(requst,pk):
    try:
        suborder=SubOrder.objects.filter(id=int(pk))
        DataSerializer=SubOrderSerializer(suborder,many=True)
        if(len(DataSerializer.data)==1):
            return Response(DataSerializer.data,status=status.HTTP_200_OK)
        else:
            return Response({'detail':f'sorry we havent sub order {pk}'},status=status.HTTP_204_NO_CONTENT)

    except:
        return Response({'detail':f'sorry we havent sub order {pk}'},status=status.HTTP_204_NO_CONTENT)
 
# all routes
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetRoutes(requst):
    Routes={
        '':'welcome',
        'api/routes/':'see all possable routes',
        'api/users/':"see all users ",
        'api/items/':"see all items",
         'api/items/<str:pk>':"see one item",
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
