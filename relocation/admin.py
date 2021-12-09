from django.contrib import admin
from .models import Housing


@admin.register(Housing)
class HousingAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'city',)
    list_filter = ('type', 'city', 'university',)
    fieldsets = (
        ('Basic info', {'fields': ('name', 'type',)}),
        ('Contacts', {'fields': ('address', 'phone', 'city',)}),
        ('Relations', {'fields': ('university',)}),
    )
    search_fields = ('name',)
    ordering = ('name', 'id',)
