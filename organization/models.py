from django.contrib.auth.models import AbstractUser
from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    is_main = models.BooleanField(default=False)  # To identify the main organization

    def __str__(self):
        return self.name

class Role(models.Model):
    NAME_CHOICES = (
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer')
    )
    name = models.CharField(max_length=50, choices=NAME_CHOICES)  # Name with choices admin, editor, and viewer.
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="users", null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.organization.name if self.organization else 'No Organization'})"
