from django.urls import path
from .views import *

urlpatterns = [
    path('saveprototype', savePrototype),
    path('getprototype', getPrototype),
    path('setprototype', setPrototype),
    path('deleteprototype', deletePrototype),
    path('getdesign', getDesign),
    path('rename', rename),
]