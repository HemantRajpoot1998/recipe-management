from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL

# Create your models here.
class Profile(models.Model):
    USER_ROLES = (
        ('creator', 'Creator'),
        ('viewer', 'Viewer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='viewer')

    def __str__(self):
        return f"{self.user.username} - {self.role}"