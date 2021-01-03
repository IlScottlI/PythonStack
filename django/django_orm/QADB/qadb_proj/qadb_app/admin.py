from django.contrib import admin

# Register your models here.
from .models import Sector, SubSector, ProductFamily, Category, OtherIndividuals, ProductType, AdditionalDetail, Action, ActionCAPA, QADB

admin.site.register([Sector, SubSector, ProductFamily, Category,
                     OtherIndividuals, ProductType, AdditionalDetail, Action, ActionCAPA, QADB])
