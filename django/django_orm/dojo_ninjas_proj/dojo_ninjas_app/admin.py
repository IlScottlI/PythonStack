from django.contrib import admin

# Register your models here.

from .models import Dojo, Ninja

admin.site.register(Dojo)
admin.site.register(Ninja)
