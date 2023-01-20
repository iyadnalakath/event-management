from django.contrib import admin
from .models import *

# Register your models here.

class AreaAdmin(admin.ModelAdmin):
    list_display=(
        'area'

    )