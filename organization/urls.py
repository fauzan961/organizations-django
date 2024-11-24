from django.urls import path
from django.contrib.auth.views import LoginView
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='/organizations/', permanent=False)),
    path("organizations/", views.organization_list, name="organization_list"),
    path("organizations/create/", views.organization_create, name="organization_create"),
    path('organizations/update/<int:pk>/', views.organization_update, name='organization_update'),
    path('organizations/delete/<int:pk>/', views.organization_delete, name='organization_delete'),
    path("users/", views.user_management, name="user_management"),
    path("users/assign-role/", views.assign_role, name="assign_role"),
    path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]
