"""
URL configuration for fundi_platform project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from services import views as services_views

urlpatterns = [
    # Custom admin dashboard URLs (must be before Django admin to avoid catch-all)
    path('admin/dashboard/', services_views.admin_dashboard, name='admin_dashboard'),
    path('admin/bookings/', services_views.admin_bookings, name='admin_bookings'),
    path('admin/booking/<int:booking_id>/', services_views.admin_booking_detail, name='admin_booking_detail'),
    path('admin/booking/<int:booking_id>/edit/', services_views.admin_edit_booking, name='admin_edit_booking'),
    path('admin/booking/<int:booking_id>/delete/', services_views.admin_delete_booking, name='admin_delete_booking'),
    path('admin/fundis/', services_views.admin_fundis, name='admin_fundis'),
    path('admin/fundi/<int:fundi_id>/', services_views.admin_fundi_detail, name='admin_fundi_detail'),
    path('admin/fundi/add/', services_views.admin_add_fundi, name='admin_add_fundi'),
    path('admin/fundi/<int:fundi_id>/edit/', services_views.admin_edit_fundi, name='admin_edit_fundi'),
    path('admin/fundi/<int:fundi_id>/delete/', services_views.admin_delete_fundi, name='admin_delete_fundi'),
    path('admin/customers/', services_views.admin_customers, name='admin_customers'),
    path('admin/customer/add/', services_views.admin_add_customer, name='admin_add_customer'),
    path('admin/customer/<int:user_id>/', services_views.admin_customer_detail, name='admin_customer_detail'),
    path('admin/fundi-activity/', services_views.admin_fundi_activity, name='admin_fundi_activity'),
    path('admin/payments/', services_views.admin_payments, name='admin_payments'),
    path('admin/payment/<int:payment_id>/', services_views.admin_payment_detail, name='admin_payment_detail'),
    path('admin/payment/<int:payment_id>/approve/', services_views.admin_approve_payment, name='admin_approve_payment'),
    path('admin/payment/<int:payment_id>/update-status/', services_views.admin_update_payment_status, name='admin_update_payment_status'),
    
    # Django admin (catch-all must be last)
    path('admin/', admin.site.urls),
    path('', include('services.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)






