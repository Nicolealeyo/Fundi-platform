from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Fundi, Service, Booking, Review, Payment


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    is_fundi = forms.BooleanField(required=False, label='Register as Fundi')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 
                  'phone_number', 'address', 'is_fundi')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.address = self.cleaned_data['address']
        user.is_fundi = self.cleaned_data['is_fundi']
        if commit:
            user.save()
        return user


class FundiProfileForm(forms.ModelForm):
    class Meta:
        model = Fundi
        fields = ['category', 'experience_years', 'hourly_rate', 'bio', 'profile_picture', 'is_available']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['fundi', 'service', 'description', 'address', 'booking_date', 'estimated_hours']
        widgets = {
            'service': forms.Select(attrs={
                'class': 'form-control form-control-modern',
                'style': 'cursor: pointer;'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control form-control-modern',
                'placeholder': 'Describe your service needs in detail...'
            }),
            'address': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control form-control-modern',
                'placeholder': 'Enter the service address...'
            }),
            'booking_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control form-control-modern'
            }),
            'estimated_hours': forms.NumberInput(attrs={
                'class': 'form-control form-control-modern',
                'min': '1',
                'placeholder': '1'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        fundi = kwargs.pop('fundi', None)
        super().__init__(*args, **kwargs)
        self.fields['fundi'].queryset = Fundi.objects.filter(is_available=True)
        
        # Filter services by fundi's category and ensure default services exist
        if fundi:
            # Get or create default services for the fundi's category
            category = fundi.category
            default_services = {
                'plumber': [
                    ('Pipe Repair', 'Fix leaking pipes and plumbing issues'),
                    ('Drain Cleaning', 'Unclog and clean drains'),
                    ('Toilet Installation', 'Install new toilets'),
                    ('Water Heater Repair', 'Fix water heater problems'),
                    ('General Plumbing', 'General plumbing services'),
                ],
                'electrician': [
                    ('Wiring Installation', 'Install electrical wiring'),
                    ('Light Fixture Installation', 'Install light fixtures'),
                    ('Outlet Repair', 'Fix electrical outlets'),
                    ('Circuit Breaker Repair', 'Fix circuit breaker issues'),
                    ('General Electrical Work', 'General electrical services'),
                ],
                'cleaner': [
                    ('House Cleaning', 'Complete house cleaning service'),
                    ('Office Cleaning', 'Office space cleaning'),
                    ('Deep Cleaning', 'Thorough deep cleaning'),
                    ('Window Cleaning', 'Window and glass cleaning'),
                    ('Carpet Cleaning', 'Carpet and upholstery cleaning'),
                ],
                'carpenter': [
                    ('Furniture Repair', 'Repair damaged furniture'),
                    ('Cabinet Installation', 'Install cabinets'),
                    ('Door Installation', 'Install doors'),
                    ('Shelf Installation', 'Install shelves'),
                    ('General Carpentry', 'General carpentry work'),
                ],
                'painter': [
                    ('Interior Painting', 'Paint interior walls'),
                    ('Exterior Painting', 'Paint exterior walls'),
                    ('Room Painting', 'Paint specific rooms'),
                    ('Wall Repair & Paint', 'Repair and paint walls'),
                    ('General Painting', 'General painting services'),
                ],
                'other': [
                    ('General Service', 'General service request'),
                    ('Consultation', 'Service consultation'),
                    ('Other', 'Other service needs'),
                ],
            }
            
            # Get or create services for this category
            services_for_category = []
            for service_name, service_desc in default_services.get(category, default_services['other']):
                service, created = Service.objects.get_or_create(
                    name=service_name,
                    category=category,
                    defaults={'description': service_desc}
                )
                services_for_category.append(service)
            
            # Also include any existing services for this category
            existing_services = Service.objects.filter(category=category)
            all_services = list(set(list(services_for_category) + list(existing_services)))
            
            self.fields['service'].queryset = Service.objects.filter(id__in=[s.id for s in all_services])
            self.fields['service'].empty_label = "Select a service..."


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 1}),
        }


class PaymentForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=15, 
        required=False,
        label='M-Pesa Phone Number',
        help_text='Enter any M-Pesa registered phone number. Format: 254XXXXXXXXX or 07XXXXXXXX',
        widget=forms.TextInput(attrs={
            'placeholder': '254712345678 or 0712345678',
            'list': 'test-numbers'
        })
    )
    
    class Meta:
        model = Payment
        fields = ['payment_method', 'phone_number']
        widgets = {
            'payment_method': forms.Select(attrs={'onchange': 'togglePhoneField()'}),
        }
    
    def __init__(self, *args, **kwargs):
        booking = kwargs.pop('booking', None)
        super().__init__(*args, **kwargs)
        if booking:
            self.booking = booking
    
    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        phone_number = cleaned_data.get('phone_number')
        
        if payment_method == 'mpesa' and not phone_number:
            raise forms.ValidationError({'phone_number': 'Phone number is required for M-Pesa payments.'})
        
        return cleaned_data


class ContactFundiForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=True)
    
    def __init__(self, *args, **kwargs):
        fundi = kwargs.pop('fundi', None)
        super().__init__(*args, **kwargs)
        if fundi:
            self.fundi = fundi
