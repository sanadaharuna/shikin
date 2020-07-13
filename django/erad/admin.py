from django.contrib import admin

from .models import Suppl


@admin.register(Suppl)
class SupplAdmin(admin.ModelAdmin):
    pass
