from django.urls import path
from .consumer import dataConsumer

ws_urlpatterns=[
    path('ws/',dataConsumer.as_asgi())
]
