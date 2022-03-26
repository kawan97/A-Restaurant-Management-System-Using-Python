from urllib import request
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User
import json

from .serializers import ItemSerializer,FeedbackSerializer,ProfileSerializer,ActionSerializer,EquipmentSerializer,PaymentSerializer,UserWithNameSerializer ,UserSerializer,OrderSerializer,SubOrderSerializer,OrderItemSerializer,AllTableSerializer
from app.models import Item,Order,SubOrder,OrderItem,SubItem,Table,Action,Payment,Equipment,Profile,Feedback

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



# -----------------------------
# get all users
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUsers(requst):
    try:
        if requst.user.profile.user_role != 'admin':
            return Response({'permission':'sorry you are not allowed to perform that action','role':requst.user.profile.user_role},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        Users=User.objects.all()
        DataSerializer=UserWithNameSerializer(Users,many=True)
        # print(requst.user.profile.date)
        return Response({'success':'that is all users','data':DataSerializer.data},status=status.HTTP_200_OK)
    except:
        return Response({'detail':'sorry you have error'},status=status.HTTP_204_NO_CONTENT)

# get  users actions
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUserActions(requst,stdate,enddate,userid):
    try:
        if requst.user.profile.user_role != 'admin':
            return Response({'permission':'sorry you are not allowed to perform that action','role':requst.user.profile.user_role},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        # payment=Payment.objects.all()
        # payment=Payment.objects.filter(date__gte='2022-03-09',date__lte='2022-03-20')
        action=Action.objects.filter(date__gte=stdate,date__lte=enddate,User__id=userid)

        DataSerializer=ActionSerializer(action,many=True)
        return Response({'success':f'successfully get all action','data':DataSerializer.data},status=status.HTTP_200_OK) 
    except:
        return Response({'detail':f'sorry we havent action '},status=status.HTTP_204_NO_CONTENT)

# get all Items
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetItems(requst):
    try:
        if requst.user.profile.user_role != 'admin' or requst.user.profile.user_role != 'captain':
            return Response({'permission':'sorry you are not allowed to perform that action','role':requst.user.profile.user_role},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        items=Item.objects.all()
        DataSerializer=ItemSerializer(items,many=True)
        # print(requst.user.profile.date)
        return Response({'data':DataSerializer.data},status=status.HTTP_200_OK)
    except:
         return Response({'detail':'sorry we havent any item'},status=status.HTTP_204_NO_CONTENT)
  

# get one Items
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetItem(requst,pk):
    try:
        if requst.user.profile.user_role != 'admin' or requst.user.profile.user_role != 'captain':
            return Response({'permission':'sorry you are not allowed to perform that action','role':requst.user.profile.user_role},status=status.HTTP_405_METHOD_NOT_ALLOWED)
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
    try:
        if requst.user.profile.user_role != 'admin' or requst.user.profile.user_role != 'captain':
            return Response({'permission':'sorry you are not allowed to perform that action','role':requst.user.profile.user_role},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        tables=Table.objects.all()
        # .prefetch_related('ordertable')
        # tables=Table.objects.get(id='2').ordertable.filter(status='notpayed')
        # tables=Table.objects.filter(ordertable__status__contains='notpayed')
        # tables=tables.filter(ordertable__id='3')
        # .prefetch_related('ordertable_set')
        # tables=tables.filter(status='empty')
        # .filter(suborderorder__status='ordering')
        # print(tables)
        DataSerializer=AllTableSerializer(tables,many=True)
        return Response(DataSerializer.data,status=status.HTTP_200_OK)
    except:
        return Response({'detail':'sorry we havent any order'},status=status.HTTP_204_NO_CONTENT)
# get one table with order
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetTable(requst,pk):
    try:
        if requst.user.profile.user_role != 'admin' or requst.user.profile.user_role != 'captain':
            return Response({'permission':'sorry you are not allowed to perform that action','role':requst.user.profile.user_role},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        tables=Table.objects.get(id=pk).ordertable.filter(status='notpayed')
        DataSerializer=OrderSerializer(tables,many=True)
        return Response(DataSerializer.data,status=status.HTTP_200_OK)
    except:
        return Response({'detail':'sorry we havent any order'},status=status.HTTP_204_NO_CONTENT)

# get orders
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetOrders(requst):
    try:
        if requst.user.profile.user_role != 'admin' or requst.user.profile.user_role != 'captain':
            return Response({'permission':'sorry you are not allowed to perform that action','role':requst.user.profile.user_role},status=status.HTTP_405_METHOD_NOT_ALLOWED)
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
        if requst.user.profile.user_role != 'admin'  or requst.user.profile.user_role != 'captain':
            return Response({'permission':'sorry you are not allowed to perform that action','role':requst.user.profile.user_role},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        orders=Order.objects.filter(id=int(pk)).prefetch_related('suborderorder')
        # orders=orders.filter(suborderorder__status='ordering')
        # .filter(suborderorder__status='ordering')
        # print(orders)
        DataSerializer=OrderSerializer(orders,many=True)
        if(len(DataSerializer.data)==1):
            return Response({'success':'you get order','data':DataSerializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'detail':f'sorry we havent  order {pk}'},status=status.HTTP_204_NO_CONTENT)

    except:
        return Response({'detail':f'sorry we havent  order {pk}'},status=status.HTTP_204_NO_CONTENT)
  # get single Sub Order
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetSubOrder(requst,pk):
    try:
        if requst.user.profile.user_role != 'admin' or requst.user.profile.user_role != 'captain':
            return Response({'permission':'sorry you are not allowed to perform that action','role':requst.user.profile.user_role},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        suborder=SubOrder.objects.filter(id=int(pk))
        DataSerializer=SubOrderSerializer(suborder,many=True)
        if(len(DataSerializer.data)==1):
            return Response({'success':'you get that sub order','data':DataSerializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'detail':f'sorry we havent sub order {pk}'},status=status.HTTP_204_NO_CONTENT)

    except:
        return Response({'detail':f'sorry we havent sub order {pk}'},status=status.HTTP_204_NO_CONTENT)
# get  Sub Order when status = sendingtochef
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAllSubOrders(requst):
    try:
        if requst.user.profile.user_role != 'chef':
            return Response({'permission':'sorry you are not allowed to perform that action','role':requst.user.profile.user_role},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        suborder=SubOrder.objects.filter(status='sendingtochef')
        DataSerializer=SubOrderSerializer(suborder,many=True)
        return Response({'success':f'successfully get all sub order','data':DataSerializer.data},status=status.HTTP_200_OK) 
    except:
        return Response({'detail':f'sorry we havent sub order '},status=status.HTTP_204_NO_CONTENT)
 # get  Sub Order when status = orderisready
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAllWaiterSubOrders(requst):
    try:
        if requst.user.profile.user_role != 'waiter':
            return Response({'permission':'sorry you are not allowed to perform that action','role':requst.user.profile.user_role},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        suborder=SubOrder.objects.filter(status='orderisready')
        DataSerializer=SubOrderSerializer(suborder,many=True)
        return Response({'success':f'successfully get all sub order','data':DataSerializer.data},status=status.HTTP_200_OK) 
    except:
        return Response({'detail':f'sorry we havent sub order '},status=status.HTTP_204_NO_CONTENT)
# get all payment by date
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAllPayments(requst,stdate,enddate):
    try:
        if requst.user.profile.user_role != 'admin':
            return Response({'permission':'sorry you are not allowed to perform that action','role':requst.user.profile.user_role},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        payment=Payment.objects.filter(date__gte=stdate,date__lte=enddate)
        DataSerializer=PaymentSerializer(payment,many=True)
        return Response({'success':f'successfully get all payment','data':DataSerializer.data},status=status.HTTP_200_OK) 
    except:
        return Response({'detail':f'sorry we havent payments '},status=status.HTTP_204_NO_CONTENT)

# get  all equipment by date
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAllEquipment(requst,stdate,enddate):
    try:
        if requst.user.profile.user_role != 'admin':
            return Response({'permission':'sorry you are not allowed to perform that action','role':requst.user.profile.user_role},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        allequipent=Equipment.objects.filter(date__gte=stdate,date__lte=enddate)
        DataSerializer=EquipmentSerializer(allequipent,many=True)
        return Response({'success':f'successfully get all Equipment','data':DataSerializer.data},status=status.HTTP_200_OK) 
    except:
        return Response({'detail':f'sorry we havent Equipment '},status=status.HTTP_204_NO_CONTENT)

#Get Monthly Report
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetMonthlyReport(requst,year,month):
    try:
        if requst.user.profile.user_role != 'admin':
            return Response({'permission':'sorry you are not allowed to perform that action','role':requst.user.profile.user_role},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        from datetime import datetime
        startdate=datetime.fromisoformat(year+'-'+month+'-01')
        enddate=add_months(startdate,1)
        enddate=datetime.fromisoformat(str(enddate))
        payment=Payment.objects.filter(date__gte=startdate,date__lte=enddate)
        PaymentDataSerializer=PaymentSerializer(payment,many=True)
        equipent=Equipment.objects.filter(date__gte=startdate,date__lte=enddate)
        EquipmentDataSerializer=EquipmentSerializer(equipent,many=True)
        profile=Profile.objects.filter(status='active')
        ProfileDataSerializer=ProfileSerializer(profile,many=True) 
        sumofpayments=0
        for i in range(len(PaymentDataSerializer.data)):
            sumofpayments=sumofpayments+int(PaymentDataSerializer.data[i]['total'])
        sumofuser=0
        for i in range(len(ProfileDataSerializer.data)):
            sumofuser=sumofuser+int(ProfileDataSerializer.data[i]['user_salary'])
        sumofequipent=0
        for i in range(len(EquipmentDataSerializer.data)):
            sumofequipent=sumofequipent+int(EquipmentDataSerializer.data[i]['total'])
        return Response({'success':f'successfully get report','data':{'user':{'total':sumofuser,'length':len(ProfileDataSerializer.data)},'equipent':{'total':sumofequipent,'length':len(EquipmentDataSerializer.data)} ,'payment':{'total':sumofpayments,'length':len(PaymentDataSerializer.data)}}},status=status.HTTP_200_OK) 
    except:
        return Response({'detail':f'sorry we havent Equipment '},status=status.HTTP_204_NO_CONTENT)
def add_months(sourcedate, months):
    import datetime
    import calendar
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

# add single Order
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddOrder(requst):
    try:
        if requst.user.profile.user_role != 'admin' or requst.user.profile.user_role != 'captain':
            return Response({'permission':'sorry you are not allowed to perform that action','role':requst.user.profile.user_role},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        import random
        FormData=json.loads((requst.body.decode()))
        tableId=FormData['tableid']
        print(tableId)
        table=Table.objects.get(id=int(tableId))
        if(table.status=='reserved'):
            return Response({'error':f'sorry  table {table.name} is reserved'},status=status.HTTP_400_BAD_REQUEST)
        table.status='reserved'
        table.save()
        newOrder=Order(status='notpayed',User=requst.user,Table=table)
        newOrder.save()
        newFeedback=Feedback(Order=newOrder,key=random.randrange(1000000, 99999999, 1))
        newFeedback.save()
        DataSerializer=OrderSerializer(newOrder,many=False)
        return Response({'success':f'you successfully add one  order','data':DataSerializer.data},status=status.HTTP_201_CREATED)
    except:
        return Response({'detail':f'sorry you have an error'},status=status.HTTP_400_BAD_REQUEST)
# add single equipment
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddEquipment(requst):
    try:
        if requst.user.profile.user_role != 'admin':
            return Response({'permission':'sorry you are not allowed to perform that action','role':requst.user.profile.user_role},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        FormData=json.loads((requst.body.decode()))
        name=FormData['name']
        total=FormData['total']
        newEquipment=Equipment(name=name,User=requst.user,total=total)
        newEquipment.save()
        DataSerializer=EquipmentSerializer(newEquipment,many=False)
        return Response({'success':f'you successfully add one  Equipment','data':DataSerializer.data},status=status.HTTP_201_CREATED)
    except:
        return Response({'detail':f'sorry you have an error'},status=status.HTTP_400_BAD_REQUEST)

# add single feedback
@api_view(['POST'])
def AddFeedback(requst,orderid,key):
    try:
        FormData=json.loads((requst.body.decode()))
        userfeedback=FormData['text']
        feedback=Feedback.objects.get(Order__id=int(orderid),key=key)
        if(feedback.status=='answered'):
            return Response({'answered':f'sorry you add feedback to this order'},status=status.HTTP_400_BAD_REQUEST)
        feedback.status='answered'
        feedback.text=userfeedback
        feedback.save()
        DataSerializer=FeedbackSerializer(feedback,many=False)
        return Response({'success':f'you successfully add feedback','data':DataSerializer.data},status=status.HTTP_201_CREATED)
    except:
        return Response({'detail':f'sorry you have an error'},status=status.HTTP_400_BAD_REQUEST)

# add single Sub Order
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddSubOrder(requst,pk):
    try:
        if requst.user.profile.user_role != 'admin' or requst.user.profile.user_role != 'captain':
            return Response({'permission':'sorry you are not allowed to perform that action','role':requst.user.profile.user_role},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        order=Order.objects.get(id=int(pk))
        newSubOrder=SubOrder(status='ordering',User=requst.user,Order=order,Table=order.Table)
        newSubOrder.save()
        DataSerializer=SubOrderSerializer(newSubOrder,many=False)
        return Response({'success':f'you successfully add one sub order','data':DataSerializer.data},status=status.HTTP_201_CREATED)
    except:
        return Response({'detail':f'sorry you have an error'},status=status.HTTP_400_BAD_REQUEST)
# update single sub order status
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UpdateSubOrderStatus(requst,pk):
    try:
        FormData=json.loads((requst.body.decode()))
        suborderstatus=FormData['suborderstatus']
        if(suborderstatus =='sendingtochef'):
            if requst.user.profile.user_role != 'captain':
                return Response({'permission':'sorry you are not allowed to perform that action','role':requst.user.profile.user_role},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if(suborderstatus =='orderisready'):
            if requst.user.profile.user_role != 'chef':
                return Response({'permission':'sorry you are not allowed to perform that action','role':requst.user.profile.user_role},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if(suborderstatus =='waiterserving'):
            if requst.user.profile.user_role != 'waiter':
                return Response({'permission':'sorry you are not allowed to perform that action','role':requst.user.profile.user_role},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        suborder=SubOrder.objects.get(id=int(pk))
        suborder.status=suborderstatus
        suborder.save()
        DataSerializer=SubOrderSerializer(suborder,many=False)
        newAction=Action(SubOrder=suborder,User=requst.user,type=suborderstatus)
        newAction.save()
        return Response({'success':f'you successfully update sub order status','data':DataSerializer.data},status=status.HTTP_201_CREATED)
    except:
        return Response({'detail':f'sorry you have an error'},status=status.HTTP_400_BAD_REQUEST)

# update single  order status
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UpdateOrderStatus(requst,pk):
    try:
        if requst.user.profile.user_role != 'admin':
            return Response({'permission':'sorry you are not allowed to perform that action','role':requst.user.profile.user_role},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        order=Order.objects.get(id=int(pk))
        if(order.status=='payed'):
            return Response({'payed':f'sorry this order is payed'},status=status.HTTP_400_BAD_REQUEST)
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
        return Response({'success':f'you successfully pay order','data':DataSerializer.data['suborderorder']},status=status.HTTP_201_CREATED)
    except:
        return Response({'detail':f'sorry you have an error'},status=status.HTTP_400_BAD_REQUEST)

# add single item to single Sub Order
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddOrderItem(requst,pk):
    try:
        if requst.user.profile.user_role != 'admin' or requst.user.profile.user_role != 'captain':
            return Response({'permission':'sorry you are not allowed to perform that action','role':requst.user.profile.user_role},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        FormData=json.loads((requst.body.decode()))
        subItemId=FormData['subitemid']
        subitem=SubItem.objects.get(id=int(subItemId))
        suborder=SubOrder.objects.get(id=int(pk))
        neworderitem=OrderItem(User=requst.user,Order=suborder.Order,Table=suborder.Table,SubOrder=suborder,SubItem=subitem)
        neworderitem.save()
        # print(neworderitem)
        DataSerializer=OrderItemSerializer(neworderitem,many=False)
        return Response({'success':f'you successfully add one order item ','data':DataSerializer.data},status=status.HTTP_201_CREATED)
    except:
        return Response({'detail':f'sorry you have an error'},status=status.HTTP_400_BAD_REQUEST)

# all routes
@api_view(['GET'])
def GetRoutes(requst):
    Routes={
        '':'GET:welcome',
        'admin':'go to admin panel',
        'api/routes/':'GET: see all possable routes',
        'api/login/':'POST: you can login and get access token body:username,password',
        'api/users/':"GET:see all users ",
        'api/items/':"GET:see all items and sub item",
        'api/items/<str:pk>':"GET:see one item",
        'api/orders/':"GET:see all orders with suborders and sub items",
        'api/orders/<str:pk>':"GET:see one order with suborders and sub items",
        'api/tables/':"GET:see all tables without order",
        'api/tables/<str:pk>':"GET:see that order on this table and order is notpayed",
        'api/suborders/':'GET: see all that suborder where status is sendingtochef',
        'api/waitersuborders/':'GET: see all that suborder where status is orderisready',
        'api/suborders/<str:pk>':"GET:see one suborder and all order item",
        'api/suborder/<str:pk>':"POST:add suborder  to one order",
        'api/orderitem/<str:pk>':"POST:add order item  to one suborder body:subitemid",
        'api/order/':"POST:add order to one table body:tableid",
        'api/suborderupdate/<str:pk>':"POST:update suborder status body:suborderstatus",
        'api/orderupdate/<str:pk>':"POST:update order status",
        'api/payments/<str:stdate>/<str:enddate>/':'GET get all payemnt between 2 date',
        'api/useraction/<str:stdate>/<str:enddate>/<str:userid>/':'see action by date and user',
        'api/equipment/':'POST : add one  equipment body:name,total',
        'api/equipments/<str:stdate>/<str:enddate>/':'GET : see all  equipment by date',
        'api/monthlyreport/<str:year>/<str:month>/':'get monthly report',

    }

    return Response(Routes,status=status.HTTP_200_OK)


# home
@api_view(['GET'])
def GetHome(requst):
    msg={
        'home':'welcome to home',
    }

    return Response(msg,status=status.HTTP_200_OK)
