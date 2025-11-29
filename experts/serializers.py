from rest_framework import serializers
from .models import SuggestionPost, Question, Answer

class AnswerSerializer(serializers.ModelSerializer):
    expert_name = serializers.ReadOnlyField(source='expert.username')

    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ('expert', 'created_at')

class QuestionSerializer(serializers.ModelSerializer):
    farmer_name = serializers.ReadOnlyField(source='farmer.username')
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ('farmer', 'created_at', 'is_answered')

class SuggestionPostSerializer(serializers.ModelSerializer):
    expert_name = serializers.ReadOnlyField(source='expert.username')

    class Meta:
        model = SuggestionPost
        fields = '__all__'
        read_only_fields = ('expert', 'created_at')
