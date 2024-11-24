from django import forms
from .models import Organization, CustomUser, Role

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ["name", "address", "is_main"]

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "organization", "role"]

class RoleAssignmentForm(forms.Form):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all())
    role = forms.ModelChoiceField(queryset=Role.objects.all())
    
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['username', 'email']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        
        return password_confirm
