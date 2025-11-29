from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile, ExpertRegistrationRequest
from django.utils import timezone

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )


@admin.register(ExpertRegistrationRequest)
class ExpertRegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'status', 'created_at', 'reviewed_at')
    list_filter = ('status',)
    search_fields = ('email', 'username')
    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        approved_count = 0
        for expert_request in queryset.filter(status='pending'):
            # Create the user
            user = User.objects.create_user(
                username=expert_request.username,
                email=expert_request.email,
                password=expert_request.password,  # Django will hash this
                role='expert'
            )
            
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
            
            approved_count += 1
        
        self.message_user(request, f'{approved_count} expert registration(s) approved.')
    approve_requests.short_description = 'Approve selected expert registrations'

    def reject_requests(self, request, queryset):
        rejected_count = queryset.filter(status='pending').update(
            status='rejected',
            reviewed_at=timezone.now()
        )
        self.message_user(request, f'{rejected_count} expert registration(s) rejected.')
    reject_requests.short_description = 'Reject selected expert registrations'
