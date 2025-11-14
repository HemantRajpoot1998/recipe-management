from django.contrib import admin
from users.models import Profile

# Register your models here.
admin.site.register(Profile)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
   