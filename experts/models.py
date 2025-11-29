from django.db import models
from django.conf import settings

class SuggestionPost(models.Model):
    expert = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='suggestions')
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.CharField(max_length=200, help_text="Comma separated tags")
    image = models.ImageField(upload_to='suggestions/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions')
    content = models.TextField()
    is_answered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question by {self.farmer.username}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    expert = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.expert.username}"
