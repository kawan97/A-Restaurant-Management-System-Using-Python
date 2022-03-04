
from django.contrib import admin
from django.urls import path
from . import view

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
# )
urlpatterns = [
     path('', view.GetHome),
    path('api/login/', view.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('admin/', admin.site.urls),
    path('api/routes/', view.GetRoutes),
    path('api/users/', view.GetUsers),

]
