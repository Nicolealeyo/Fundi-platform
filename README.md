# Fundi Platform - Home Service Booking Platform

A fully functional Django-based web application for booking home services (plumbers, electricians, cleaners, etc.) in your neighborhood. Similar to popular service booking apps like "Fundi App".

## Features

✅ **Fundi Listings**
- Browse available fundis (service providers) by category
- Search and filter fundis by name, category, and price
- View detailed fundi profiles with ratings and reviews

✅ **Reviews & Ratings**
- Customers can leave reviews and ratings after completed bookings
- Display average ratings and review counts on fundi profiles
- View all reviews for each fundi

✅ **Service Request & Booking**
- Create service booking requests
- Track booking status (Pending, Confirmed, In Progress, Completed, Cancelled)
- Fundis can update booking status
- Customers and fundis can view all their bookings

✅ **Payment & Tracking**
- Payment integration support (ready for Stripe/M-Pesa integration)
- Track payment status
- View booking history and payment history

## Technology Stack

- **Backend**: Django 4.2.7
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Database**: SQLite (default, can be changed to PostgreSQL/MySQL)
- **Forms**: Django Crispy Forms with Bootstrap 5

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd Project
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and go to: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## Usage Guide

### For Customers

1. **Register/Login**: Create an account or login
2. **Browse Fundis**: Go to "Find Fundis" to see available service providers
3. **View Profile**: Click on a fundi to see their profile, ratings, and reviews
4. **Book Service**: Click "Book Service" to create a booking request
5. **Make Payment**: After booking is confirmed, make payment
6. **Leave Review**: After service completion, leave a review and rating

### For Fundis (Service Providers)

1. **Register as Fundi**: During registration, check "Register as Fundi"
2. **Create Profile**: Complete your fundi profile with category, experience, rates, etc.
3. **Dashboard**: View your bookings, statistics, and manage your profile
4. **Update Status**: Update booking status as you work on jobs
5. **View Reviews**: See customer reviews and ratings on your profile

## Project Structure

```
Project/
├── fundi_platform/          # Main project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── services/                # Main app
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── forms.py             # Form definitions
│   ├── urls.py              # App URL patterns
│   └── admin.py             # Admin configuration
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   └── services/            # App-specific templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User-uploaded files
├── manage.py                # Django management script
└── requirements.txt         # Python dependencies
```

## Models

- **User**: Custom user model with customer/fundi distinction
- **Fundi**: Service provider profiles with category, rates, availability
- **Service**: Service categories (plumber, electrician, cleaner, etc.)
- **Booking**: Service booking requests with status tracking
- **Review**: Customer reviews and ratings
- **Payment**: Payment records and tracking

## Payment Integration

The platform is ready for payment gateway integration. Currently, payments are marked as "completed" automatically. To integrate with real payment providers:

1. **Stripe**: Update `STRIPE_PUBLISHABLE_KEY` and `STRIPE_SECRET_KEY` in settings.py
2. **M-Pesa**: Add M-Pesa API integration in the payment view
3. **Other**: Modify `create_payment` view in `services/views.py`

## Future Enhancements

- Real-time notifications
- Chat/messaging between customers and fundis
- Advanced search with location-based filtering
- Mobile app API
- Email notifications
- Booking calendar/scheduling
- Multiple payment gateway support

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please contact: support@fundiplatform.com






