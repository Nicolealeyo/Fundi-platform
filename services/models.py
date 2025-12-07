from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    is_fundi = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username


class Service(models.Model):
    CATEGORY_CHOICES = [
        ('plumber', 'Plumber'),
        ('electrician', 'Electrician'),
        ('cleaner', 'Cleaner'),
        ('carpenter', 'Carpenter'),
        ('painter', 'Painter'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    
    def __str__(self):
        return self.name


class Fundi(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='fundi_profile')
    category = models.CharField(max_length=50, choices=Service.CATEGORY_CHOICES)
    experience_years = models.IntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='fundi_profiles/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def average_rating(self):
        reviews = Review.objects.filter(booking__fundi=self)
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 2)
        return 0.0
    
    @property
    def total_reviews(self):
        return Review.objects.filter(booking__fundi=self).count()
    
    def __str__(self):
        return f"{self.user.username} - {self.get_category_display()}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_bookings')
    fundi = models.ForeignKey(Fundi, on_delete=models.CASCADE, related_name='fundi_bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    description = models.TextField()
    address = models.TextField()
    booking_date = models.DateTimeField()
    estimated_hours = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def total_cost(self):
        return self.fundi.hourly_rate * self.estimated_hours
    
    def __str__(self):
        return f"{self.customer.username} - {self.fundi.user.username} - {self.service.name}"


class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.booking} - {self.rating} stars"


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('mpesa', 'M-Pesa'),
        ('cash', 'Cash'),
    ]
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    transaction_id = models.CharField(max_length=200, blank=True)
    merchant_request_id = models.CharField(max_length=200, blank=True, help_text='M-Pesa Merchant Request ID')
    checkout_request_id = models.CharField(max_length=200, blank=True, help_text='M-Pesa Checkout Request ID')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Payment for {self.booking} - {self.amount}"

