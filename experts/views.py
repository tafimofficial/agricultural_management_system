from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions
from .models import SuggestionPost, Question, Answer
from .serializers import SuggestionPostSerializer, QuestionSerializer, AnswerSerializer

class SuggestionPostViewSet(viewsets.ModelViewSet):
    queryset = SuggestionPost.objects.all().order_by('-created_at')
    serializer_class = SuggestionPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(expert=self.request.user)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('-created_at')
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        question = serializer.validated_data['question']
        question.is_answered = True
        question.save()
        serializer.save(expert=self.request.user)
        
        # Create notification for farmer
        from notifications.models import Notification
        Notification.objects.create(
            user=question.farmer,
            message=f"Expert {self.request.user.username} answered your question: {question.content[:30]}...",
            link="/experts/questions/"
        )

@login_required
def questions_list(request):
    return render(request, 'experts/questions.html')

@login_required
def suggestions_list(request):
    return render(request, 'experts/suggestions.html')

@login_required
def expert_directory(request):
    return render(request, 'experts/directory.html')
