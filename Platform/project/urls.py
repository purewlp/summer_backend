from django.urls import path
from .views import *

urlpatterns=[
    path('create',createProject),
    path('delete',deleteProject),
    path('recover',recoverProject),
    path('rename',renameProject),
    path('list/',list),
]