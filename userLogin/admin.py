from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserKeys

# admin.site.register(User, UserAdmin)
# Register your models here.


@admin.register(UserKeys)
class UserKeysAdmin(admin.ModelAdmin):
    list_display = ('user', 'publickey')
