from django.contrib import admin

# Register your models here.
from .models import Users


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email_address', 'age')
    search_fields = ('title', 'email_address', 'last_name', 'first_name')
    list_per_page = 25


admin.site.register(Users, UserAdmin)
