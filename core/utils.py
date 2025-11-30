from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

def assign_role_permissions(user):
    """
    Assigns default permissions to a user based on their role.
    """
    role = user.role
    permissions_to_add = []

    if role == 'farmer':
        # Farmers can manage their listings and ask questions
        codenames = [
            'add_producelisting', 'change_producelisting', 'delete_producelisting', 'view_producelisting',
            'add_question', 'view_question',
            'view_produce', # View daily prices
        ]
    elif role == 'buyer':
        # Buyers can order and view listings
        codenames = [
            'add_order', 'view_order',
            'view_producelisting',
            'view_produce',
        ]
    elif role == 'expert':
        # Experts can manage suggestions and answer questions
        codenames = [
            'add_suggestionpost', 'change_suggestionpost', 'delete_suggestionpost', 'view_suggestionpost',
            'view_question', 'add_answer', 'view_answer',
            'view_produce',
        ]
    elif role == 'admin':
        # Admins can manage produce and users
        codenames = [
            'add_produce', 'change_produce', 'delete_produce', 'view_produce',
            'add_user', 'change_user', 'delete_user', 'view_user',
            # Add other admin permissions as needed
        ]
    else:
        return

    for codename in codenames:
        try:
            perm = Permission.objects.get(codename=codename)
            permissions_to_add.append(perm)
        except Permission.DoesNotExist:
            print(f"Warning: Permission {codename} not found.")
            continue

    if permissions_to_add:
        user.user_permissions.add(*permissions_to_add)
