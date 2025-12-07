from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Avg, Count, Sum
from django.core.paginator import Paginator
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django import forms
import json
from datetime import timedelta
from urllib.parse import urlparse
from .models import User, Fundi, Service, Booking, Review, Payment
from .forms import CustomUserCreationForm, FundiProfileForm, BookingForm, ReviewForm, PaymentForm, ContactFundiForm
from .mpesa_utils import initiate_stk_push


def home(request):
    """Home page with featured fundis and categories"""
    categories = Service.CATEGORY_CHOICES
    # Get all available fundis, prioritizing those with ratings but including new ones
    featured_fundis = Fundi.objects.filter(is_available=True).annotate(
        avg_rating=Avg('fundi_bookings__review__rating'),
        review_count=Count('fundi_bookings__review')
    ).order_by('-review_count', '-avg_rating', '-created_at')[:12]  # Show up to 12 fundis, including new ones
    
    # Get recent testimonials/reviews for home page (visible to all, no login required)
    recent_reviews = Review.objects.select_related(
        'booking__fundi__user', 
        'booking__customer', 
        'booking__service'
    ).order_by('-created_at')[:10]  # Get more reviews for slider
    
    context = {
        'categories': categories,
        'featured_fundis': featured_fundis,
        'testimonials': recent_reviews,
    }
    return render(request, 'services/home.html', context)


def register(request):
    """User registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Account created successfully! Welcome {username}')
                if user.is_fundi:
                    return redirect('create_fundi_profile')
                return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'services/register.html', {'form': form})


@login_required
def create_fundi_profile(request):
    """Create fundi profile after registration"""
    if hasattr(request.user, 'fundi_profile'):
        messages.info(request, 'You already have a fundi profile!')
        return redirect('fundi_dashboard')
    
    if request.method == 'POST':
        form = FundiProfileForm(request.POST, request.FILES)
        if form.is_valid():
            fundi = form.save(commit=False)
            fundi.user = request.user
            # Ensure new fundis are automatically available
            if not fundi.pk:  # Only for new fundis
                fundi.is_available = True
            fundi.save()
            messages.success(request, 'Fundi profile created successfully!')
            return redirect('fundi_dashboard')
    else:
        form = FundiProfileForm()
    return render(request, 'services/create_fundi_profile.html', {'form': form})


@login_required
def fundi_list(request):
    """List all available fundis with filters"""
    fundis = Fundi.objects.filter(is_available=True)
    category = request.GET.get('category')
    search = request.GET.get('search')
    sort_by = request.GET.get('sort', 'rating')
    
    if category:
        fundis = fundis.filter(category=category)
    
    if search:
        fundis = fundis.filter(
            Q(user__username__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(bio__icontains=search)
        )
    
    # Annotate with average rating
    fundis = fundis.annotate(
        avg_rating=Avg('fundi_bookings__review__rating'),
        review_count=Count('fundi_bookings__review')
    )
    
    if sort_by == 'rating':
        fundis = fundis.order_by('-avg_rating', '-review_count', '-created_at')
    elif sort_by == 'price_low':
        fundis = fundis.order_by('hourly_rate')
    elif sort_by == 'price_high':
        fundis = fundis.order_by('-hourly_rate')
    else:
        fundis = fundis.order_by('-created_at')
    
    paginator = Paginator(fundis, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': Service.CATEGORY_CHOICES,
        'selected_category': category,
        'search_query': search,
        'sort_by': sort_by,
    }
    return render(request, 'services/fundi_list.html', context)


def fundi_detail(request, fundi_id):
    """Fundi profile page"""
    fundi = get_object_or_404(Fundi, id=fundi_id)
    
    # Get all reviews with pagination
    all_reviews = Review.objects.filter(booking__fundi=fundi).order_by('-created_at')
    paginator = Paginator(all_reviews, 5)
    page_number = request.GET.get('review_page')
    reviews_page = paginator.get_page(page_number)
    
    # Get recent bookings
    recent_bookings = Booking.objects.filter(fundi=fundi).order_by('-created_at')[:10]
    total_completed = Booking.objects.filter(fundi=fundi, status='completed').count()
    
    # Check if user has completed bookings with this fundi (for review button)
    can_review = False
    completed_booking_for_review = None
    if request.user.is_authenticated and not request.user.is_fundi:
        completed_booking_for_review = Booking.objects.filter(
            customer=request.user,
            fundi=fundi,
            status='completed'
        ).exclude(review__isnull=False).first()
        if completed_booking_for_review:
            can_review = True
    
    context = {
        'fundi': fundi,
        'reviews_page': reviews_page,
        'recent_bookings': recent_bookings,
        'total_completed': total_completed,
        'can_review': can_review,
        'completed_booking_for_review': completed_booking_for_review,
    }
    return render(request, 'services/fundi_detail.html', context)


@login_required
def create_booking(request, fundi_id):
    """Create a service booking"""
    fundi = get_object_or_404(Fundi, id=fundi_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, fundi=fundi)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.fundi = fundi
            booking.save()
            messages.success(request, 'Booking request created successfully!')
            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = BookingForm(fundi=fundi)
        form.fields['fundi'].widget = forms.HiddenInput()
        form.fields['fundi'].initial = fundi
    
    context = {
        'form': form,
        'fundi': fundi,
    }
    return render(request, 'services/create_booking.html', context)


@login_required
def booking_detail(request, booking_id):
    """View booking details"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if user has permission to view this booking
    if booking.customer != request.user and booking.fundi.user != request.user:
        messages.error(request, 'You do not have permission to view this booking.')
        return redirect('home')
    
    # Check if payment exists
    payment = None
    try:
        payment = booking.payment
    except Payment.DoesNotExist:
        pass
    
    # Check if review exists
    review = None
    try:
        review = booking.review
    except Review.DoesNotExist:
        pass
    
    # Ensure all status choices are available - explicitly convert to list
    status_choices = list(Booking.STATUS_CHOICES)
    
    context = {
        'booking': booking,
        'payment': payment,
        'review': review,
        'status_choices': status_choices,
    }
    return render(request, 'services/booking_detail.html', context)


@login_required
def my_bookings(request):
    """User's bookings"""
    if request.user.is_fundi:
        bookings = Booking.objects.filter(fundi__user=request.user).order_by('-created_at')
    else:
        bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')
    
    context = {
        'bookings': bookings,
    }
    return render(request, 'services/my_bookings.html', context)


@login_required
def update_booking_status(request, booking_id):
    """Update booking status (for fundis)"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.fundi.user != request.user:
        messages.error(request, 'You do not have permission to update this booking.')
        return redirect('home')
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Booking.STATUS_CHOICES):
            booking.status = new_status
            booking.save()
            messages.success(request, f'Booking status updated to {booking.get_status_display()}')
    
    return redirect('booking_detail', booking_id=booking_id)


@login_required
def create_payment(request, booking_id):
    """Create payment for a booking"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.customer != request.user:
        messages.error(request, 'You do not have permission to pay for this booking.')
        return redirect('home')
    
    # Check if payment already exists
    if hasattr(booking, 'payment'):
        messages.info(request, 'Payment already exists for this booking.')
        return redirect('booking_detail', booking_id=booking_id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, booking=booking)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.amount = booking.total_cost
            phone_number = form.cleaned_data.get('phone_number', '')
            
            # Handle M-Pesa payment
            if form.cleaned_data['payment_method'] == 'mpesa':
                # Format phone number and amount
                phone_number = form.cleaned_data.get('phone_number', '')
                amount = float(booking.total_cost)
                
                # Create callback URL - use settings if available, otherwise build from request
                callback_url = settings.MPESA_CALLBACK_URL
                
                # If callback URL is not set or is localhost, try to build from request
                if not callback_url or 'localhost' in callback_url or '127.0.0.1' in callback_url:
                    # For local development, user must use ngrok or set MPESA_CALLBACK_URL in .env
                    if 'localhost' in request.get_host() or '127.0.0.1' in request.get_host():
                        messages.error(request, 
                            'M-Pesa requires a publicly accessible HTTPS URL for callbacks. '
                            'For local testing, please use ngrok. See MPESA_SETUP.md for instructions.')
                        return render(request, 'services/create_payment.html', {
                            'form': form,
                            'booking': booking,
                        })
                    callback_url = request.build_absolute_uri('/mpesa/callback/')
                
                # Ensure callback URL uses HTTPS (M-Pesa requirement)
                if callback_url.startswith('http://'):
                    callback_url = callback_url.replace('http://', 'https://', 1)
                
                # Account reference (booking ID)
                account_reference = f"BOOKING_{booking.id}"
                
                # Transaction description
                transaction_desc = f"Payment for {booking.service.name} - Booking #{booking.id}"
                
                # Initiate STK push
                stk_response = initiate_stk_push(
                    phone_number=phone_number,
                    amount=amount,
                    account_reference=account_reference,
                    transaction_desc=transaction_desc,
                    callback_url=callback_url
                )
                
                if stk_response.get('success'):
                    # Save payment with M-Pesa details
                    payment.merchant_request_id = stk_response.get('merchant_request_id', '')
                    payment.checkout_request_id = stk_response.get('checkout_request_id', '')
                    payment.transaction_id = stk_response.get('checkout_request_id', '')
                    payment.status = 'pending'
                    payment.save()
                    
                    customer_message = stk_response.get('customer_message', 'STK push sent successfully!')
                    messages.success(request, customer_message)
                    messages.info(request, f'Please check your phone {phone_number} and enter your M-Pesa PIN to complete the payment.')
                    
                    # Log success for debugging
                    print(f"STK Push Success - MerchantRequestID: {payment.merchant_request_id}, CheckoutRequestID: {payment.checkout_request_id}")
                else:
                    # Payment creation failed - show detailed error
                    error_msg = stk_response.get('error', 'Failed to initiate payment')
                    error_code = stk_response.get('error_code', 'Unknown')
                    
                    # More user-friendly error messages
                    if 'access token' in error_msg.lower():
                        error_msg = 'Authentication failed. Please check your M-Pesa credentials.'
                    elif 'invalid' in error_msg.lower() or 'invalid' in str(error_code).lower():
                        error_msg = f'Invalid request: {error_msg}. Please check phone number format (should be 254XXXXXXXXX).'
                    
                    messages.error(request, f'M-Pesa payment failed: {error_msg}')
                    
                    # Log error for debugging
                    print(f"STK Push Failed - Error: {error_msg}, Code: {error_code}")
                    print(f"Full response: {stk_response}")
                    
                    return render(request, 'services/create_payment.html', {
                        'form': form,
                        'booking': booking,
                    })
            else:
                # For cash payment method
                payment.status = 'completed'
                payment.completed_at = timezone.now()
                payment.save()
                
                # Automatically update booking status to completed when payment is completed
                if booking.status != 'completed':
                    booking.status = 'completed'
                    booking.save()
                
                messages.success(request, 'Payment completed successfully!')
            
            return redirect('booking_detail', booking_id=booking_id)
    else:
        form = PaymentForm(booking=booking)
    
    context = {
        'form': form,
        'booking': booking,
    }
    return render(request, 'services/create_payment.html', context)


@login_required
def create_review(request, booking_id):
    """Create a review for a completed booking"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.customer != request.user:
        messages.error(request, 'You do not have permission to review this booking.')
        return redirect('home')
    
    if booking.status != 'completed':
        messages.error(request, 'You can only review completed bookings.')
        return redirect('booking_detail', booking_id=booking_id)
    
    # Check if review already exists
    if hasattr(booking, 'review'):
        messages.info(request, 'You have already reviewed this booking.')
        return redirect('booking_detail', booking_id=booking_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('booking_detail', booking_id=booking_id)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'booking': booking,
    }
    return render(request, 'services/create_review.html', context)


@login_required
def fundi_dashboard(request):
    """Fundi dashboard"""
    if not request.user.is_fundi:
        messages.error(request, 'You are not registered as a fundi.')
        return redirect('home')
    
    try:
        fundi = request.user.fundi_profile
    except Fundi.DoesNotExist:
        return redirect('create_fundi_profile')
    
    bookings = Booking.objects.filter(fundi=fundi).order_by('-created_at')[:10]
    total_bookings = Booking.objects.filter(fundi=fundi).count()
    completed_bookings = Booking.objects.filter(fundi=fundi, status='completed').count()
    pending_bookings = Booking.objects.filter(fundi=fundi, status='pending').count()
    
    context = {
        'fundi': fundi,
        'bookings': bookings,
        'total_bookings': total_bookings,
        'completed_bookings': completed_bookings,
        'pending_bookings': pending_bookings,
    }
    return render(request, 'services/fundi_dashboard.html', context)


@login_required
def edit_fundi_profile(request):
    """Edit fundi profile"""
    try:
        fundi = request.user.fundi_profile
    except Fundi.DoesNotExist:
        messages.error(request, 'You need to create a fundi profile first.')
        return redirect('create_fundi_profile')
    
    if request.method == 'POST':
        form = FundiProfileForm(request.POST, request.FILES, instance=fundi)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('fundi_dashboard')
    else:
        form = FundiProfileForm(instance=fundi)
    
    context = {
        'form': form,
        'fundi': fundi,
    }
    return render(request, 'services/edit_fundi_profile.html', context)


def contact_fundi(request, fundi_id):
    """Contact fundi form"""
    fundi = get_object_or_404(Fundi, id=fundi_id)
    
    if request.method == 'POST':
        form = ContactFundiForm(request.POST, fundi=fundi)
        if form.is_valid():
            # In production, send email notification here
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # For now, just show success message
            messages.success(request, f'Your message has been sent to {fundi.user.get_full_name() or fundi.user.username}. They will contact you soon!')
            return redirect('fundi_detail', fundi_id=fundi_id)
    else:
        form = ContactFundiForm(fundi=fundi)
        # Pre-fill form if user is logged in
        if request.user.is_authenticated:
            form.fields['name'].initial = request.user.get_full_name() or request.user.username
            form.fields['email'].initial = request.user.email
            if request.user.phone_number:
                form.fields['phone'].initial = request.user.phone_number
    
    context = {
        'form': form,
        'fundi': fundi,
    }
    return render(request, 'services/contact_fundi.html', context)


# Admin Dashboard Views
def is_admin(user):
    """Check if user is admin (staff or superuser)"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard overview"""
    # Statistics
    total_bookings = Booking.objects.count()
    total_fundis = Fundi.objects.count()
    total_customers = User.objects.filter(is_fundi=False).count()
    total_users = User.objects.count()
    
    # Recent activity
    recent_bookings = Booking.objects.select_related('customer', 'fundi__user', 'service').order_by('-created_at')[:10]
    recent_fundis = Fundi.objects.select_related('user').order_by('-created_at')[:10]
    recent_users = User.objects.order_by('-date_joined')[:10]
    
    # Status counts
    pending_bookings = Booking.objects.filter(status='pending').count()
    completed_bookings = Booking.objects.filter(status='completed').count()
    active_fundis = Fundi.objects.filter(is_available=True).count()
    
    # Payment statistics
    total_payments = Payment.objects.count()
    completed_payments = Payment.objects.filter(status='completed').count()
    pending_payments = Payment.objects.filter(status='pending').count()
    failed_payments = Payment.objects.filter(status='failed').count()
    total_revenue = Payment.objects.filter(status='completed').aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'total_bookings': total_bookings,
        'total_fundis': total_fundis,
        'total_customers': total_customers,
        'total_users': total_users,
        'pending_bookings': pending_bookings,
        'completed_bookings': completed_bookings,
        'active_fundis': active_fundis,
        'total_payments': total_payments,
        'completed_payments': completed_payments,
        'pending_payments': pending_payments,
        'failed_payments': failed_payments,
        'total_revenue': total_revenue,
        'recent_bookings': recent_bookings,
        'recent_fundis': recent_fundis,
        'recent_users': recent_users,
    }
    return render(request, 'services/admin/dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def admin_bookings(request):
    """Admin view all bookings"""
    bookings = Booking.objects.select_related('customer', 'fundi__user', 'service').order_by('-created_at')
    
    # Filters
    status_filter = request.GET.get('status')
    search_query = request.GET.get('search')
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    if search_query:
        bookings = bookings.filter(
            Q(customer__username__icontains=search_query) |
            Q(customer__email__icontains=search_query) |
            Q(fundi__user__username__icontains=search_query) |
            Q(service__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    paginator = Paginator(bookings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
        'status_choices': Booking.STATUS_CHOICES,
    }
    return render(request, 'services/admin/bookings.html', context)


@login_required
@user_passes_test(is_admin)
def admin_booking_detail(request, booking_id):
    """Admin view booking detail"""
    booking = get_object_or_404(Booking.objects.select_related('customer', 'fundi__user', 'service'), id=booking_id)
    
    # Get related payment and review
    payment = None
    review = None
    try:
        payment = booking.payment
    except Payment.DoesNotExist:
        pass
    
    try:
        review = booking.review
    except Review.DoesNotExist:
        pass
    
    context = {
        'booking': booking,
        'payment': payment,
        'review': review,
    }
    return render(request, 'services/admin/booking_detail.html', context)


@login_required
@user_passes_test(is_admin)
def admin_edit_booking(request, booking_id):
    """Admin edit booking"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Booking.STATUS_CHOICES):
            booking.status = status
            booking.save()
            messages.success(request, f'Booking status updated to {booking.get_status_display()}')
            return redirect('admin_booking_detail', booking_id=booking_id)
    
    return redirect('admin_booking_detail', booking_id=booking_id)


@login_required
@user_passes_test(is_admin)
def admin_delete_booking(request, booking_id):
    """Admin delete booking"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking deleted successfully!')
        return redirect('admin_bookings')
    
    context = {'booking': booking}
    return render(request, 'services/admin/delete_booking.html', context)


@login_required
@user_passes_test(is_admin)
def admin_fundis(request):
    """Admin view all fundis"""
    fundis = Fundi.objects.select_related('user').annotate(
        avg_rating=Avg('fundi_bookings__review__rating'),
        total_bookings=Count('fundi_bookings')
    ).order_by('-created_at')
    
    # Filters
    category_filter = request.GET.get('category')
    search_query = request.GET.get('search')
    availability_filter = request.GET.get('availability')
    
    if category_filter:
        fundis = fundis.filter(category=category_filter)
    
    if availability_filter == 'available':
        fundis = fundis.filter(is_available=True)
    elif availability_filter == 'unavailable':
        fundis = fundis.filter(is_available=False)
    
    if search_query:
        fundis = fundis.filter(
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(bio__icontains=search_query)
        )
    
    paginator = Paginator(fundis, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'category_filter': category_filter,
        'search_query': search_query,
        'availability_filter': availability_filter,
        'category_choices': Service.CATEGORY_CHOICES,
    }
    return render(request, 'services/admin/fundis.html', context)


@login_required
@user_passes_test(is_admin)
def admin_fundi_detail(request, fundi_id):
    """Admin view fundi detail"""
    fundi = get_object_or_404(Fundi.objects.select_related('user'), id=fundi_id)
    bookings = Booking.objects.filter(fundi=fundi).order_by('-created_at')[:10]
    total_bookings = Booking.objects.filter(fundi=fundi).count()
    
    context = {
        'fundi': fundi,
        'bookings': bookings,
        'total_bookings': total_bookings,
    }
    return render(request, 'services/admin/fundi_detail.html', context)


@login_required
@user_passes_test(is_admin)
def admin_add_fundi(request):
    """Admin add new fundi"""
    if request.method == 'POST':
        # Create user first
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        phone_number = request.POST.get('phone_number', '')
        
        # Check if user exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'services/admin/add_fundi.html', {
                'category_choices': Service.CATEGORY_CHOICES,
            })
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return render(request, 'services/admin/add_fundi.html', {
                'category_choices': Service.CATEGORY_CHOICES,
            })
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            is_fundi=True
        )
        
        # Create fundi profile
        form = FundiProfileForm(request.POST, request.FILES)
        if form.is_valid():
            fundi = form.save(commit=False)
            fundi.user = user
            fundi.save()
            messages.success(request, f'Fundi {user.username} created successfully!')
            return redirect('admin_fundi_detail', fundi_id=fundi.id)
        else:
            user.delete()
            messages.error(request, 'Error creating fundi profile. Please check the form.')
    else:
        form = FundiProfileForm()
    
    context = {
        'form': form,
        'category_choices': Service.CATEGORY_CHOICES,
    }
    return render(request, 'services/admin/add_fundi.html', context)


@login_required
@user_passes_test(is_admin)
def admin_edit_fundi(request, fundi_id):
    """Admin edit fundi"""
    fundi = get_object_or_404(Fundi.objects.select_related('user'), id=fundi_id)
    
    if request.method == 'POST':
        # Update user info
        fundi.user.first_name = request.POST.get('first_name', '')
        fundi.user.last_name = request.POST.get('last_name', '')
        fundi.user.email = request.POST.get('email', '')
        fundi.user.phone_number = request.POST.get('phone_number', '')
        fundi.user.save()
        
        # Update fundi profile
        form = FundiProfileForm(request.POST, request.FILES, instance=fundi)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fundi updated successfully!')
            return redirect('admin_fundi_detail', fundi_id=fundi.id)
    else:
        form = FundiProfileForm(instance=fundi)
    
    context = {
        'form': form,
        'fundi': fundi,
        'category_choices': Service.CATEGORY_CHOICES,
    }
    return render(request, 'services/admin/edit_fundi.html', context)


@login_required
@user_passes_test(is_admin)
def admin_delete_fundi(request, fundi_id):
    """Admin delete fundi"""
    fundi = get_object_or_404(Fundi.objects.select_related('user'), id=fundi_id)
    
    if request.method == 'POST':
        username = fundi.user.username
        fundi.user.delete()  # This will also delete the fundi due to CASCADE
        messages.success(request, f'Fundi {username} deleted successfully!')
        return redirect('admin_fundis')
    
    context = {'fundi': fundi}
    return render(request, 'services/admin/delete_fundi.html', context)


@login_required
@user_passes_test(is_admin)
def admin_customers(request):
    """Admin view all customers"""
    customers = User.objects.filter(is_fundi=False).order_by('-date_joined')
    
    # Filters
    search_query = request.GET.get('search')
    
    if search_query:
        customers = customers.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )
    
    # Annotate with booking count
    customers = customers.annotate(booking_count=Count('customer_bookings'))
    
    paginator = Paginator(customers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'services/admin/customers.html', context)


@login_required
@user_passes_test(is_admin)
def admin_add_customer(request):
    """Admin add new customer"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        phone_number = request.POST.get('phone_number', '')
        address = request.POST.get('address', '')
        
        # Check if user exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'services/admin/add_customer.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return render(request, 'services/admin/add_customer.html')
        
        # Create customer user (is_fundi=False)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address,
            is_fundi=False
        )
        
        messages.success(request, f'Customer {user.username} created successfully!')
        return redirect('admin_customer_detail', user_id=user.id)
    
    return render(request, 'services/admin/add_customer.html')


@login_required
@user_passes_test(is_admin)
def admin_customer_detail(request, user_id):
    """Admin view customer detail"""
    customer = get_object_or_404(User, id=user_id, is_fundi=False)
    bookings = Booking.objects.filter(customer=customer).order_by('-created_at')
    total_bookings = bookings.count()
    
    paginator = Paginator(bookings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'customer': customer,
        'page_obj': page_obj,
        'total_bookings': total_bookings,
    }
    return render(request, 'services/admin/customer_detail.html', context)


@login_required
@user_passes_test(is_admin)
def admin_fundi_activity(request):
    """Admin view fundi login/registration activity"""
    # Get all fundis with their registration date and last login
    fundis = Fundi.objects.select_related('user').annotate(
        total_bookings=Count('fundi_bookings'),
        avg_rating=Avg('fundi_bookings__review__rating')
    ).order_by('-created_at')
    
    # Get recently registered fundis (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_registrations = fundis.filter(created_at__gte=thirty_days_ago)
    
    # Get fundis who logged in recently
    recent_logins = fundis.filter(user__last_login__gte=thirty_days_ago)
    
    context = {
        'fundis': fundis,
        'recent_registrations': recent_registrations,
        'recent_logins': recent_logins,
        'total_fundis': fundis.count(),
    }
    return render(request, 'services/admin/fundi_activity.html', context)


@login_required
@user_passes_test(is_admin)
def admin_payments(request):
    """Admin view all payments"""
    payments = Payment.objects.select_related('booking__customer', 'booking__fundi__user', 'booking__service').order_by('-created_at')
    
    # Filters
    status_filter = request.GET.get('status')
    method_filter = request.GET.get('method')
    search_query = request.GET.get('search')
    
    if status_filter:
        payments = payments.filter(status=status_filter)
    
    if method_filter:
        payments = payments.filter(payment_method=method_filter)
    
    if search_query:
        payments = payments.filter(
            Q(booking__customer__username__icontains=search_query) |
            Q(booking__fundi__user__username__icontains=search_query) |
            Q(transaction_id__icontains=search_query) |
            Q(merchant_request_id__icontains=search_query) |
            Q(checkout_request_id__icontains=search_query)
        )
    
    paginator = Paginator(payments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_revenue = Payment.objects.filter(status='completed').aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'method_filter': method_filter,
        'search_query': search_query,
        'status_choices': Payment.STATUS_CHOICES,
        'method_choices': Payment.PAYMENT_METHOD_CHOICES,
        'total_revenue': total_revenue,
    }
    return render(request, 'services/admin/payments.html', context)


@login_required
@user_passes_test(is_admin)
def admin_payment_detail(request, payment_id):
    """Admin view payment detail"""
    payment = get_object_or_404(
        Payment.objects.select_related('booking__customer', 'booking__fundi__user', 'booking__service'),
        id=payment_id
    )
    booking = payment.booking
    
    context = {
        'payment': payment,
        'booking': booking,
    }
    return render(request, 'services/admin/payment_detail.html', context)


@login_required
@user_passes_test(is_admin)
def admin_approve_payment(request, payment_id):
    """Admin approve/complete a payment"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    if request.method == 'POST':
        # Update payment status to completed
        payment.status = 'completed'
        payment.completed_at = timezone.now()
        payment.save()
        
        # Automatically update booking status to completed
        booking = payment.booking
        if booking.status != 'completed':
            booking.status = 'completed'
            booking.save()
        
        messages.success(request, f'Payment #{payment.id} approved and marked as completed!')
        return redirect('admin_payment_detail', payment_id=payment.id)
    
    return redirect('admin_payment_detail', payment_id=payment.id)


@login_required
@user_passes_test(is_admin)
def admin_update_payment_status(request, payment_id):
    """Admin update payment status"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Payment.STATUS_CHOICES):
            payment.status = new_status
            if new_status == 'completed' and not payment.completed_at:
                payment.completed_at = timezone.now()
            
            # If marking as completed, also update booking
            if new_status == 'completed':
                booking = payment.booking
                if booking.status != 'completed':
                    booking.status = 'completed'
                    booking.save()
            
            payment.save()
            messages.success(request, f'Payment status updated to {payment.get_status_display()}')
        else:
            messages.error(request, 'Invalid payment status')
    
    return redirect('admin_payment_detail', payment_id=payment.id)

