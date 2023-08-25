from django.urls import re_path

import chat
from chat import consumers

websocket_urlpatterns = [
    re_path('ws/chat/message/text/', chat.consumers.ChatConsumer.as_asgi()),
]
