from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, ChatRoomViewSet, ChatMessageViewSet, get_or_create_chat_room, send_chat_message

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'chat-rooms', ChatRoomViewSet, basename='chatroom')
router.register(r'messages', ChatMessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    path('chat/room/<int:user_id>/', get_or_create_chat_room, name='get_chat_room'),
    path('chat/send/', send_chat_message, name='send_message'),
]
