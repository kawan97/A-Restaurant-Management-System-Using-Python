
from django.contrib import admin
from django.urls import path
from . import view

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
# )
urlpatterns = [
    path('finalreport/<str:pk>/<str:mytoken>/', view.FinalReport),
    path('', view.GetHome),
    path('api/login/', view.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('admin/', admin.site.urls),
    path('api/routes/', view.GetRoutes),
    path('api/users/', view.GetUsers),
    path('api/items/', view.GetItems),
    path('api/items/<str:pk>/', view.GetItem),
    path('api/orders/', view.GetOrders),
    path('api/orders/<str:pk>/', view.GetOrder),
    path('api/tables/', view.GetTables),
    path('api/tables/<str:pk>', view.GetTable),
    path('api/suborders/', view.GetAllSubOrders),
    path('api/waitersuborders/', view.GetAllWaiterSubOrders),
    path('api/suborders/<str:pk>/', view.GetSubOrder),
    path('api/suborder/<str:pk>/', view.AddSubOrder),
    path('api/orderitem/<str:pk>/', view.AddOrderItem),
    path('api/order/', view.AddOrder),
    path('api/suborderupdate/<str:pk>/', view.UpdateSubOrderStatus),
    path('api/orderupdate/<str:pk>/', view.UpdateOrderStatus),
    path('api/payments/<str:stdate>/<str:enddate>/', view.GetAllPayments),
    path('api/useraction/<str:stdate>/<str:enddate>/<str:userid>/', view.GetUserActions),
    path('api/equipment/', view.AddEquipment),
    path('api/equipments/<str:stdate>/<str:enddate>/', view.GetAllEquipment),
    path('api/monthlyreport/<str:year>/<str:month>/', view.GetMonthlyReport),
    path('api/feedback/<str:orderid>/<str:key>/', view.AddFeedback),



]
