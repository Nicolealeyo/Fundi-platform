from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import mpesa_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='services/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Fundi related
    path('fundis/', views.fundi_list, name='fundi_list'),
    path('fundi/<int:fundi_id>/', views.fundi_detail, name='fundi_detail'),
    path('fundi/<int:fundi_id>/contact/', views.contact_fundi, name='contact_fundi'),
    path('fundi/create-profile/', views.create_fundi_profile, name='create_fundi_profile'),
    path('fundi/dashboard/', views.fundi_dashboard, name='fundi_dashboard'),
    path('fundi/edit-profile/', views.edit_fundi_profile, name='edit_fundi_profile'),
    
    # Booking related
    path('booking/create/<int:fundi_id>/', views.create_booking, name='create_booking'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:booking_id>/update-status/', views.update_booking_status, name='update_booking_status'),
    
    # Payment related
    path('payment/create/<int:booking_id>/', views.create_payment, name='create_payment'),
    
    # M-Pesa callback/webhook
    path('mpesa/callback/', mpesa_views.mpesa_callback, name='mpesa_callback'),
    
    # Review related
    path('review/create/<int:booking_id>/', views.create_review, name='create_review'),
]

