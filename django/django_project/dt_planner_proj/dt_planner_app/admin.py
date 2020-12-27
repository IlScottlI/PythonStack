from django.contrib import admin
from admin_views.admin import AdminViews
from dt_planner_app.models import User, Calendar, Plant, Business, Module, Department, Area, Type, Reason, Approver, Question, Track, History, Comment, Locale, Response, Status, Contributor
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter
)

admin.site.register([
    Calendar,
    Plant,
    Business,
    Module,
    Department,
    Type,
    Reason,
    Approver,
    Question,
    Track,
    History,
    Comment,
    Locale,
    Response,
    Status,
    Contributor
])


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'admin', 'plant')
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = (
        ('plant', ChoiceDropdownFilter),
        ('admin', ChoiceDropdownFilter),
    )


admin.site.register(User, UserAdmin)


class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'plant')
    list_filter = (
        ('department', ChoiceDropdownFilter),
    )


admin.site.register(Area, AreaAdmin)
