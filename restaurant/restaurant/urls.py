
from django.contrib import admin
from django.urls import path
from . import view

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
# )
urlpatterns = [
    path('api/login/', view.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('admin/', admin.site.urls),
    path('routes/', view.GetRoutes),
    path('users/', view.GetUsers),

]
