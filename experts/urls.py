from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SuggestionPostViewSet, QuestionViewSet, AnswerViewSet, questions_list, suggestions_list, expert_directory


router = DefaultRouter()
router.register(r'suggestions', SuggestionPostViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# Template URLs (accessed via /experts/)
template_urlpatterns = [
    path('questions/', questions_list, name='experts_questions'),
    path('suggestions/', suggestions_list, name='experts_suggestions'),
    path('directory/', expert_directory, name='expert_directory'),
]
