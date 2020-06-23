from django.contrib import admin

from .models import Jsps


@admin.register(Jsps)
class JspsAdmin(admin.ModelAdmin):
    pass
