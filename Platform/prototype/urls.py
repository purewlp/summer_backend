from django.urls import path
from .views import *

urlpatterns = [
    path('saveprototype', savePrototype),
    path('getprototype', getPrototype),
]