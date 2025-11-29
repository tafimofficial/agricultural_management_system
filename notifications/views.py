from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Notification, ChatRoom, ChatMessage
from .serializers import NotificationSerializer, ChatRoomSerializer, ChatMessageSerializer

User = get_user_model()

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        self.get_queryset().update(is_read=True)
        return Response({'status': 'marked all as read'})

class ChatRoomViewSet(viewsets.ModelViewSet):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.chat_rooms.all()

class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = ChatMessage.objects.filter(room__participants=self.request.user).order_by('timestamp')
        room_id = self.request.query_params.get('room', None)
        if room_id:
            queryset = queryset.filter(room_id=room_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_or_create_chat_room(request, user_id):
    """Get or create a chat room between current user and target user"""
    other_user = get_object_or_404(User, id=user_id)
    
    # Find existing room
    rooms = request.user.chat_rooms.filter(participants=other_user)
    
    if rooms.exists():
        room = rooms.first()
    else:
        # Create new room
        room = ChatRoom.objects.create()
        room.participants.add(request.user, other_user)
    
    # Get messages
    messages = room.messages.all()
    messages_data = ChatMessageSerializer(messages, many=True).data
    
    return Response({
        'room_id': room.id,
        'messages': messages_data
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_chat_message(request):
    """Send a chat message"""
    recipient_id = request.data.get('recipient_id')
    content = request.data.get('content')
    room_id = request.data.get('room_id')
    
    if not content:
        return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get or create room
    if room_id:
        room = get_object_or_404(ChatRoom, id=room_id, participants=request.user)
    else:
        recipient = get_object_or_404(User, id=recipient_id)
        rooms = request.user.chat_rooms.filter(participants=recipient)
        if rooms.exists():
            room = rooms.first()
        else:
            room = ChatRoom.objects.create()
            room.participants.add(request.user, recipient)
    
    # Create message
    message = ChatMessage.objects.create(
        room=room,
        sender=request.user,
        content=content
    )
    
    # Create notification for recipient
    recipient = room.get_other_participant(request.user)
    if recipient:
        Notification.objects.create(
            user=recipient,
            message=f"{request.user.username} sent you a message",
            link=f"/chat/{room.id}/"
        )
    
    return Response(ChatMessageSerializer(message).data, status=status.HTTP_201_CREATED)
