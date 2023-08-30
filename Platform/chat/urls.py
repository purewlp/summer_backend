from django.urls import path
from chat import views

urlpatterns = [
    path('message/', views.MessageView.as_view()),
    path('list/', views.RoomList.as_view()),
    path('file/', views.FileView.as_view()),
    path('doc/', views.DocView.as_view()),
    path('doc/list/', views.DocListView.as_view()),
    path('group/make', views.GroupMakeView.as_view()),
    path('group/invite', views.GroupInviteView.as_view()),
    path('group/room/remove', views.RoomRemoveView.as_view()),
    path('group/delete', views.GroupDeleteView.as_view()),
]
