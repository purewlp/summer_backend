from django.urls import path
from .views import *

urlpatterns=[
    path('create',createProject),
    path('delete',deleteProject),
    path('recover',recoverProject),
    path('rename',renameProject),
    path('list/',list),
    path('binlist/',binList),
    path('ownlist/',ownList),
    path('deleteagain',deleteAgain),
    path('finish',finish),
    path('collect',collect),
    path('discollect',discollect),
    path('collectlist/',collectList),
    
]