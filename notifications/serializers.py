from rest_framework import serializers
from .models import Notification, ChatRoom, ChatMessage

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = ChatMessage
        fields = '__all__'

class ChatRoomSerializer(serializers.ModelSerializer):
    participants_names = serializers.StringRelatedField(many=True, source='participants')
    other_user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = '__all__'

    def get_other_user(self, obj):
        request = self.context.get('request')
        if request and request.user:
            other = obj.get_other_participant(request.user)
            return other.username if other else 'Unknown'
        return 'Unknown'

    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        return last_msg.content if last_msg else ''
