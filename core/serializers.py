from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile, ExpertRegistrationRequest

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('phone', 'address', 'avatar', 'bio', 'specialization')

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'password', 'profile', 'is_active')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user

class ExpertRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertRegistrationRequest
        fields = '__all__'
