from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib import messages
from .models import Organization, CustomUser
from .forms import OrganizationForm, RoleAssignmentForm, UserRegistrationForm


@login_required
def organization_list(request):
    organization = getattr(request.user, 'organization', None)
    role = getattr(request.user, 'role', None)

    is_main_admin = organization and organization.is_main and role and role.name == 'admin'
    if is_main_admin:
        organizations = Organization.objects.all()
    elif organization:
        organizations = Organization.objects.filter(users=request.user)
    else:
        organizations = []

    return render(
        request, 
        "organization/organization_list.html", 
        {
            "organizations": organizations,
            "can_create_organization": is_main_admin
        }
    )


@login_required
def organization_create(request):
    organization = getattr(request.user, 'organization', None)
    role = getattr(request.user, 'role', None)
    if organization and organization.is_main and role and role.name == 'admin':
        form = OrganizationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("organization_list")
        return render(request, "organization/organization_form.html", {"form": form})
    return redirect("organization_list")


@login_required
def organization_update(request, pk):
    organization = get_object_or_404(Organization, pk=pk)
    if not (request.user.organization.is_main and request.user.role and request.user.role.name == 'admin'):
        return redirect("organization_list")
    
    form = OrganizationForm(request.POST or None, instance=organization)
    if form.is_valid():
        form.save()
        messages.success(request, "Organization updated successfully.")
        return redirect("organization_list")
    return render(request, "organization/organization_form.html", {"form": form})


@login_required
def organization_delete(request, pk):
    organization = get_object_or_404(Organization, pk=pk)
    if not (request.user.organization.is_main and request.user.role and request.user.role.name == 'admin'):
        return redirect("organization_list")
    
    if request.method == "POST":
        organization.delete()
        messages.success(request, "Organization deleted successfully.")
        return redirect("organization_list")
    return render(request, "organization/organization_confirm_delete.html", {"organization": organization})


@login_required
def user_management(request):   
    print(request.user.organization)
    organization = getattr(request.user, 'organization', None)
    role = getattr(request.user, 'role', None)
    is_admin =  role and role.name == 'admin'
    if organization and organization.is_main and is_admin:
        users = CustomUser.objects.all()
    else:
        users = CustomUser.objects.filter(organization=request.user.organization)
    return render(request, "user/user_list.html", {"users": users, "can_assing_roles": is_admin})


@login_required
def assign_role(request):
    if not request.user.role or request.user.role.name != "admin":
        return redirect("organization_list")
    form = RoleAssignmentForm(request.POST or None)
    if request.user.organization and request.user.organization.is_main:
        form.fields["user"].queryset = CustomUser.objects.all()
    else:
        form.fields["user"].queryset = CustomUser.objects.filter(organization=request.user.organization)
    if form.is_valid():
        user = form.cleaned_data["user"]
        role = form.cleaned_data["role"]
        user.role = role
        user.save()
        return redirect("user_management")
    return render(request, "user/assign_role.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('organization_list')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('organization_list')
        else:
            messages.error(request, "Registration failed. Please check the errors below.")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'user/register.html', {'form': form})
