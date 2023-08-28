from django.urls import path
from .views import *

urlpatterns=[
    path('create',create),
    path('list/',list),
    path('save',save),
    path('delete',delete),
    path('detail/',detail),
    path('remind',remind),

]