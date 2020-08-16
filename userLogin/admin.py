from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser

# admin.site.register(MyUser, UserAdmin)
# Register your models here.


@admin.register(MyUser)
class MyUser(UserAdmin):
    list_display = ('username', 'public_key')
