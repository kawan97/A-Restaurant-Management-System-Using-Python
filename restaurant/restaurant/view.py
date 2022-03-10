from urllib import request
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User


from .serializers import ItemSerializer, UserSerializer,OrderSerializer,SubOrderSerializer,OrderItemSerializer,AllTableSerializer
from app.models import Item,Order,SubOrder,OrderItem,SubItem,Table,Action,Payment

# login and acces token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        from datetime import datetime, timedelta
        nine_hours_from_now = datetime.now() + timedelta(hours=9)

        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        refresh['username']=self.user.username
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['username'] = self.user.username
        data['role'] = self.user.profile.user_role
        data['expiretoken']=format(nine_hours_from_now, '%H:%M:%S')
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

# get tables
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetTables(requst):
    if True:
        tables=Table.objects.all().prefetch_related('ordertable')
        # tables=Table.objects.get(id='2').ordertable.filter(status='notpayed')
        # tables=Table.objects.filter(ordertable__status__contains='notpayed')
        tables=tables.filter(ordertable__id='3')

        # .prefetch_related('ordertable_set')
        # tables=tables.filter(status='empty')
        # .filter(suborderorder__status='ordering')
        # print(tables)
        DataSerializer=AllTableSerializer(tables,many=True)
        return Response(DataSerializer.data,status=status.HTTP_200_OK)
    # except:
    #     return Response({'detail':'sorry we havent any order'},status=status.HTTP_204_NO_CONTENT)

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
 
# add single Order
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddOrder(requst):
    try:
        FormData=requst.POST
        tableId=FormData['tableid']
        table=Table.objects.get(id=int(tableId))
        if(table.status=='reserved'):
            return Response({'detail':f'sorry  table {table.name} is reserved'},status=status.HTTP_400_BAD_REQUEST)
        table.status='reserved'
        table.save()
        newOrder=Order(status='notpayed',User=requst.user,Table=table)
        newOrder.save()
        DataSerializer=OrderSerializer(newOrder,many=False)
        return Response({'detail':f'you successfully add one  order','data':DataSerializer.data},status=status.HTTP_201_CREATED)
    except:
        return Response({'detail':f'sorry you have an error'},status=status.HTTP_400_BAD_REQUEST)

# add single Sub Order
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddSubOrder(requst,pk):
    try:
        order=Order.objects.get(id=int(pk))
        newSubOrder=SubOrder(status='ordering',User=requst.user,Order=order,Table=order.Table)
        newSubOrder.save()
        DataSerializer=SubOrderSerializer(newSubOrder,many=False)
        return Response({'detail':f'you successfully add one sub order','data':DataSerializer.data},status=status.HTTP_201_CREATED)
    except:
        return Response({'detail':f'sorry you have an error'},status=status.HTTP_400_BAD_REQUEST)
# update single sub order status
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UpdateSubOrderStatus(requst,pk):
    try:
        FormData=requst.POST
        suborderstatus=FormData['suborderstatus']
        suborder=SubOrder.objects.get(id=int(pk))
        suborder.status=suborderstatus
        suborder.save()
        DataSerializer=SubOrderSerializer(suborder,many=False)
        newAction=Action(SubOrder=suborder,User=requst.user,type=suborderstatus)
        newAction.save()
        return Response({'detail':f'you successfully update sub order status','data':DataSerializer.data},status=status.HTTP_201_CREATED)
    except:
        return Response({'detail':f'sorry you have an error'},status=status.HTTP_400_BAD_REQUEST)

# update single  order status
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UpdateOrderStatus(requst,pk):
    try:
        order=Order.objects.get(id=int(pk))
        if(order.status=='payed'):
            return Response({'detail':f'sorry this order is payed'},status=status.HTTP_400_BAD_REQUEST)
        order.status='payed'
        order.save()
        # order.Table.status='empty'
        print(order.Table)
        mytable=Table.objects.get(id=int(order.Table.id))
        mytable.status='empty'
        mytable.save()
        DataSerializer=OrderSerializer(order,many=False)
        total=0
        suborderorder=DataSerializer.data['suborderorder']
        # print(len(suborderorder))
        for i in range(len(suborderorder)):
            item=suborderorder[i]
            # print(len(item['orderitemsuborder']))
            for j in range(len(item['orderitemsuborder'])):
                newitem=item['orderitemsuborder'][j]
                # print(newitem['SubItem']['item_price'])
                total=total+int(newitem['SubItem']['item_price'])
            print('--------------')
        newAction=Payment(Order=order,User=requst.user,total=total)
        # print(str(total))
        newAction.save()
        return Response({'detail':f'you successfully pay order','data':DataSerializer.data['suborderorder']},status=status.HTTP_201_CREATED)
    except:
        return Response({'detail':f'sorry you have an error'},status=status.HTTP_400_BAD_REQUEST)

# add single item to single Sub Order
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddOrderItem(requst,pk):
    try:
        FormData=requst.POST
        subItemId=FormData['subitemid']
        subitem=SubItem.objects.get(id=int(subItemId))
        suborder=SubOrder.objects.get(id=int(pk))
        neworderitem=OrderItem(User=requst.user,Order=suborder.Order,Table=suborder.Table,SubOrder=suborder,SubItem=subitem)
        neworderitem.save()
        # print(neworderitem)
        DataSerializer=OrderItemSerializer(neworderitem,many=False)
        return Response({'detail':f'you successfully add one order item ','data':DataSerializer.data},status=status.HTTP_201_CREATED)
    except:
        return Response({'detail':f'sorry you have an error'},status=status.HTTP_400_BAD_REQUEST)

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
