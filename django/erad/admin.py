from django.contrib import admin

from .models import Erad


@admin.register(Erad)
class EradAdmin(admin.ModelAdmin):
    pass
