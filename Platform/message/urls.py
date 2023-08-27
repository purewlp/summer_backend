from django.urls import path
from .views import *

urlpatterns = [
    path('message', message),
    path('readMessage', readMessage),
    path('sendMessage', sendMessage),
    path('deleteMessage', deleteMessage),
    path('changeMessage', changeMessage),
    path('deleteAllMessage', deleteAllMessage),
    path('changeAllMessage', changeAllMessage),
    path('acceptinvitation', acceptInvitation),
    path('rejectinvitation', rejectInvitation),
]
