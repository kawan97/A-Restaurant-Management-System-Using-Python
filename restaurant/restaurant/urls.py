
from django.contrib import admin
from django.urls import path
from . import view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('routes/', view.GetRoutes),
    path('users/', view.GetUsers),

]
