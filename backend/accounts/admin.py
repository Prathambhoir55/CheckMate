from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User


# Register your models here.


admin.site.register(User)

# Register your models here.
