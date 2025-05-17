from django.contrib import admin
from .models import Profile, Car, Booking, ContactMessage, Admin, CarImage

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone_number')
    list_filter = ('user_type',)
    search_fields = ('user__username', 'phone_number')

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3
    fields = ('image', 'caption', 'is_primary')

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'category', 'daily_rate', 'is_available', 'featured_on_homepage')
    list_filter = ('category', 'make', 'is_available', 'year', 'featured_on_homepage')
    search_fields = ('make', 'model', 'license_plate', 'category')
    list_editable = ('category', 'is_available', 'featured_on_homepage')
    inlines = [CarImageInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('make', 'model', 'year', 'category', 'color', 'license_plate')
        }),
        ('Pricing & Availability', {
            'fields': ('daily_rate', 'is_available', 'featured_on_homepage')
        }),
        ('Details', {
            'fields': ('mileage', 'description', 'image')
        }),
    )

@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ('car', 'caption', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'car__make')
    search_fields = ('car__make', 'car__model', 'caption')
    
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'start_date', 'end_date', 'status', 'total_cost')
    list_filter = ('status',)
    search_fields = ('user__username', 'car__make', 'car__model')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'created_at', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('subject', 'user__username')

@admin.register(Admin)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'crud_access', 'can_approve_bookings', 'can_manage_users')
    list_filter = ('crud_access', 'can_approve_bookings', 'can_manage_users')
