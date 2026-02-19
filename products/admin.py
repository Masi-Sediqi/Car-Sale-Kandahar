# admin.py
from django.contrib import admin
from .models import *

# Inline for multiple images
class NewCarImageInline(admin.TabularInline):
    model = NewCarImage
    extra = 3  # show 3 blank image upload fields by default
    fields = ('image', 'caption', 'uploaded_at')
    readonly_fields = ('uploaded_at',)

# Main car admin
@admin.register(NewCar)
class NewCarAdmin(admin.ModelAdmin):
    list_display = ('title', 'year_of_manufacture', 'price', 'gearbox_type', 'fuel_type', 'mileage_km', 'is_activated', 'created_at')
    list_filter = ('gearbox_type', 'fuel_type', 'is_activated', 'year_of_manufacture')
    search_fields = ('title',)
    inlines = [NewCarImageInline]

# Optional: register NewCarImage separately if you want to manage images standalone
@admin.register(NewCarImage)
class NewCarImageAdmin(admin.ModelAdmin):
    list_display = ('car', 'caption', 'uploaded_at')
    search_fields = ('car__title', 'caption')

admin.site.register(Wishlist)