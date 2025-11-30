from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        # Allow session-authenticated admin users
        if self.request.user.is_authenticated and self.request.user.role == 'admin':
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import ExpertRegistrationRequest, Profile

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            
            # If registering as expert, create pending request instead
            if role == 'expert':
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password1')
                
                # Check if request already exists
                if ExpertRegistrationRequest.objects.filter(email=email).exists():
                    messages.warning(request, 'A registration request with this email already exists.')
                    return redirect('register')
                
                # Create pending request
                expert_request = ExpertRegistrationRequest.objects.create(
                    username=username,
                    email=email,
                    password=password,  # Store raw password temporarily (will be hashed when user is created)
                )
                return render(request, 'core/expert_pending.html')
            else:
                # Normal registration for farmer/buyer
                user = form.save()
                
                # Assign default permissions
                from .utils import assign_role_permissions
                assign_role_permissions(user)
                
                Profile.objects.create(user=user)
                login(request, user)
                return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    role = request.user.role
    if role == 'farmer':
        return render(request, 'farmers/dashboard.html')
    elif role == 'buyer':
        return render(request, 'buyers/dashboard.html')
    elif role == 'expert':
        return render(request, 'experts/dashboard.html')
    elif role == 'admin':
        return render(request, 'core/admin_dashboard.html')
    else:
        return render(request, 'core/dashboard.html') # Default

@login_required
def profile(request):
    # Ensure profile exists
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        # Update user info
        request.user.email = request.POST.get('email')
        
        # Update profile info
        request.user.profile.phone = request.POST.get('phone', '')
        request.user.profile.address = request.POST.get('address', '')
        request.user.profile.bio = request.POST.get('bio', '')
        
        if request.user.role == 'expert':
            request.user.profile.specialization = request.POST.get('specialization', '')
        
        # Handle avatar upload
        if 'avatar' in request.FILES:
            request.user.profile.avatar = request.FILES['avatar']
        
        # Handle password change
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password and confirm_password:
            if new_password == confirm_password:
                request.user.set_password(new_password)
                messages.success(request, 'Password changed successfully. Please login again.')
            else:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'core/profile.html')
        
        request.user.save()
        request.user.profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'core/profile.html')
