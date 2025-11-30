from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import ExpertRegistrationRequest, User, Profile

class ExpertRequestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExpertRegistrationRequest.objects.all()
    permission_classes = [permissions.IsAdminUser]
    
    def get_serializer_class(self):
        from .serializers import ExpertRequestSerializer
        return ExpertRequestSerializer
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        expert_request = self.get_object()
        
        if expert_request.status != 'pending':
            return Response({'error': 'Request already processed'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the user
        user = User.objects.create_user(
            username=expert_request.username,
            email=expert_request.email,
            password=expert_request.password,
            role='expert'
        )
        
        # Assign default permissions
        from .utils import assign_role_permissions
        assign_role_permissions(user)
        
        # Create profile
        Profile.objects.create(
            user=user,
            specialization=expert_request.specialization,
            bio=expert_request.bio
        )
        
        # Update request status
        expert_request.status = 'approved'
        expert_request.reviewed_at = timezone.now()
        expert_request.reviewed_by = request.user
        expert_request.save()
        
        return Response({'message': 'Expert approved successfully'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        expert_request = self.get_object()
        
        if expert_request.status != 'pending':
            return Response({'error': 'Request already processed'}, status=status.HTTP_400_BAD_REQUEST)
        
        expert_request.status = 'rejected'
        expert_request.reviewed_at = timezone.now()
        expert_request.reviewed_by = request.user
        expert_request.save()
        
        return Response({'message': 'Expert request rejected'})
