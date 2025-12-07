from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Fundi, Service, Booking, Review, Payment

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_fundi', 'is_staff']
    list_filter = ['is_fundi', 'is_staff', 'is_superuser']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'address', 'is_fundi')}),
    )

@admin.register(Fundi)
class FundiAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'experience_years', 'hourly_rate', 'is_available', 'average_rating']
    list_filter = ['category', 'is_available']
    search_fields = ['user__username', 'user__email', 'category']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'description']
    list_filter = ['category']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'fundi', 'service', 'status', 'booking_date', 'created_at']
    list_filter = ['status', 'booking_date']
    search_fields = ['customer__username', 'fundi__user__username']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['booking', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'status', 'payment_method', 'transaction_id', 'created_at']
    list_filter = ['status', 'payment_method']
    search_fields = ['transaction_id', 'merchant_request_id', 'checkout_request_id']

