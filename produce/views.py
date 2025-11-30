from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib import messages
from .models import Produce
from core.models import User
from django.db.models import Q
from datetime import timedelta

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def produce_list(request):
    today = timezone.now().date()
    query = request.GET.get('q')
    
    produces = Produce.objects.filter(date=today)
    
    if query:
        produces = produces.filter(name__icontains=query)
        
    context = {
        'produces': produces,
        'today': today
    }
    return render(request, 'produce/list.html', context)

@login_required
def admin_produce_list(request):
    # Check if user is admin OR has view_produce permission
    if not (request.user.role == 'admin' or request.user.has_perm('produce.view_produce')):
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')

    today = timezone.now().date()
    produces = Produce.objects.filter(date=today)
    
    if request.method == 'POST':
        if 'add_produce' in request.POST:
            if not (request.user.role == 'admin' or request.user.has_perm('produce.add_produce')):
                messages.error(request, 'You do not have permission to add produce.')
                return redirect('admin_produce_list')
                
            name = request.POST.get('name')
            price = request.POST.get('price')
            category = request.POST.get('category')
            image = request.FILES.get('image')
            
            Produce.objects.create(
                name=name,
                price_per_kg=price,
                category=category,
                image=image,
                date=today
            )
            messages.success(request, 'Produce added successfully.')
            return redirect('admin_produce_list')
            
        elif 'update_produce' in request.POST:
            if not (request.user.role == 'admin' or request.user.has_perm('produce.change_produce')):
                messages.error(request, 'You do not have permission to update produce.')
                return redirect('admin_produce_list')

            produce_id = request.POST.get('produce_id')
            produce = get_object_or_404(Produce, id=produce_id)
            produce.name = request.POST.get('name')
            produce.price_per_kg = request.POST.get('price')
            produce.category = request.POST.get('category')
            if request.FILES.get('image'):
                produce.image = request.FILES.get('image')
            produce.save()
            messages.success(request, 'Produce updated successfully.')
            return redirect('admin_produce_list')
            
        elif 'delete_produce' in request.POST:
            if not (request.user.role == 'admin' or request.user.has_perm('produce.delete_produce')):
                messages.error(request, 'You do not have permission to delete produce.')
                return redirect('admin_produce_list')

            produce_id = request.POST.get('produce_id')
            produce = get_object_or_404(Produce, id=produce_id)
            produce.delete()
            messages.success(request, 'Produce deleted successfully.')
            return redirect('admin_produce_list')
            
        elif 'clone_produce' in request.POST:
            if not (request.user.role == 'admin' or request.user.has_perm('produce.add_produce')):
                messages.error(request, 'You do not have permission to clone produce.')
                return redirect('admin_produce_list')

            date_str = request.POST.get('clone_date')
            if date_str:
                source_date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
                old_produces = Produce.objects.filter(date=source_date)
                
                count = 0
                for item in old_produces:
                    # Check if already exists for today to avoid duplicates
                    if not Produce.objects.filter(date=today, name=item.name).exists():
                        Produce.objects.create(
                            name=item.name,
                            price_per_kg=item.price_per_kg,
                            category=item.category,
                            image=item.image, # This will reference the same file
                            date=today
                        )
                        count += 1
                messages.success(request, f'{count} items cloned from {source_date}.')
            return redirect('admin_produce_list')

    context = {
        'produces': produces,
        'today': today
    }
    return render(request, 'produce/admin_produce.html', context)

@login_required
def admin_account_list(request):
    # Check if user is admin OR has view_user permission (assuming core.view_user exists or similar)
    # Since User is a custom model, permissions are core.view_user, core.add_user, etc.
    if not (request.user.role == 'admin' or request.user.has_perm('core.view_user')):
        messages.error(request, 'You do not have permission to view accounts.')
        return redirect('dashboard')

    users = User.objects.all().exclude(is_superuser=True)
    
    if request.method == 'POST':
        if 'create_account' in request.POST:
            if not (request.user.role == 'admin' or request.user.has_perm('core.add_user')):
                messages.error(request, 'You do not have permission to create accounts.')
                return redirect('admin_account_list')

            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            role = request.POST.get('role')
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password, role=role)
                
                # Assign default permissions
                from core.utils import assign_role_permissions
                assign_role_permissions(user)
                
                messages.success(request, f'Account {username} created successfully.')
            return redirect('admin_account_list')
            
        elif 'delete_account' in request.POST:
            if not (request.user.role == 'admin' or request.user.has_perm('core.delete_user')):
                messages.error(request, 'You do not have permission to delete accounts.')
                return redirect('admin_account_list')

            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, id=user_id)
            user.delete()
            messages.success(request, 'Account deleted successfully.')
            return redirect('admin_account_list')
            
        elif 'update_account' in request.POST:
            if not (request.user.role == 'admin' or request.user.has_perm('core.change_user')):
                messages.error(request, 'You do not have permission to update accounts.')
                return redirect('admin_account_list')

            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, id=user_id)
            user.role = request.POST.get('role')
            user.save()
            messages.success(request, 'Account role updated successfully.')
            return redirect('admin_account_list')

    context = {
        'users': users
    }
    return render(request, 'produce/admin_account.html', context)

@login_required
@user_passes_test(is_admin)
def admin_user_permissions(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Allow editing permissions for all users
    # if user.role != 'custom':
    #     messages.error(request, 'Permissions can only be managed for Custom role users.')
    #     return redirect('admin_account_list')

    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType
    
    # Get all permissions
    all_permissions = Permission.objects.all().select_related('content_type').order_by('content_type__app_label', 'content_type__model', 'codename')
    
    # Group permissions by content type
    permissions_by_model = {}
    for perm in all_permissions:
        # Filter relevant apps if needed, for now showing all
        model_name = f"{perm.content_type.app_label} | {perm.content_type.model}"
        if model_name not in permissions_by_model:
            permissions_by_model[model_name] = []
        permissions_by_model[model_name].append(perm)

    if request.method == 'POST':
        selected_perms = request.POST.getlist('permissions')
        user.user_permissions.set(selected_perms)
        messages.success(request, f'Permissions updated for {user.username}.')
        return redirect('admin_account_list')

    context = {
        'target_user': user,
        'permissions_by_model': permissions_by_model,
        'user_permissions_ids': set(user.user_permissions.values_list('id', flat=True))
    }
    return render(request, 'produce/admin_user_permissions.html', context)
