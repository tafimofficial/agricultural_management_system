from django.urls import path
from . import views

urlpatterns = [
    path('', views.produce_list, name='produce_list'),
    path('admin/produce/', views.admin_produce_list, name='admin_produce_list'),
    path('admin/accounts/', views.admin_account_list, name='admin_account_list'),
    path('admin/accounts/<int:user_id>/permissions/', views.admin_user_permissions, name='admin_user_permissions'),
]
