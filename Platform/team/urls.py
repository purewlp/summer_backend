from django.urls import path
from .views import *

urlpatterns=[
    path('test',test),
    path('createteam',createTeam),
    path('changerole',changeRole),
    path('invite',invite),
    path('receive',receive),
    path('remove',remove),
    path('list/',list),
    path('teamlist/',teamList),
    path('changeteam',changeTeam),
    
]