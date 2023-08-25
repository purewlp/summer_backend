from django.urls import path
from .views import *

urlpatterns=[
    path('test',test),
    path('register',register),
    path('sendcode',sendcode),
    path('login',login),
    path('logout',logout),
    path('changenickname',changeNickname)
]