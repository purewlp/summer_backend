from django.urls import path
from .views import *

urlpatterns = [
    path('message', message),
    path('readMessage', readMessage),
    path('deleteMessage', deleteMessage),
    path('changeMessage', changeMessage),
    path('deleteAllMessage', deleteAllMessage),
    path('changeAllMessage', changeAllMessage),
]
