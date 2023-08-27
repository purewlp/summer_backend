from django.urls import path
from chat import views

urlpatterns = [
    path('', views.RoomView.as_view()),
    path('message/', views.MessageView.as_view()),
    path('list/', views.RoomList.as_view()),
    path('file/', views.FileView.as_view()),
    path('doc/', views.DocView.as_view()),
    path('doc/list/', views.DocListView.as_view()),
    path('invate/', views.Invite.as_view()),

]
