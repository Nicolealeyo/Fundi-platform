# How to Access the Admin Dashboard

## Step 1: Create an Admin User

You need to have a user account with **staff** or **superuser** privileges. You have two options:

### Option A: Create a Superuser (Recommended)
Open a terminal in your project directory and run:

```bash
python manage.py createsuperuser
```

Follow the prompts to create a superuser account (username, email, password).

### Option B: Make an Existing User an Admin
If you already have a user account, you can make them an admin using Django shell:

```bash
python manage.py shell
```

Then in the shell:
```python
from services.models import User
user = User.objects.get(username='your_username')  # Replace with your username
user.is_staff = True
user.is_superuser = True
user.save()
exit()
```

## Step 2: Start the Development Server

Make sure your virtual environment is activated, then run:

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## Step 3: Access the Admin Dashboard

### Method 1: Via Navigation Bar
1. Go to `http://127.0.0.1:8000/`
2. Log in with your admin account
3. You'll see an **"Admin"** link in the navigation bar (only visible to staff/superuser)
4. Click on it to access the admin dashboard

### Method 2: Direct URL
Navigate directly to:
```
http://127.0.0.1:8000/admin/dashboard/
```

## Admin Dashboard Features

Once you're in the admin dashboard, you can:

- **View Statistics**: Total bookings, fundis, customers, users
- **Manage Bookings**: View, edit, delete all bookings
- **Manage Fundis**: View, add, edit, delete fundis
- **View Customers**: See all registered customers
- **Track Activity**: See fundi registrations and login activity

## Quick Links

- **Dashboard Overview**: `/admin/dashboard/`
- **All Bookings**: `/admin/bookings/`
- **All Fundis**: `/admin/fundis/`
- **All Customers**: `/admin/customers/`
- **Fundi Activity**: `/admin/fundi-activity/`

## Troubleshooting

**If you don't see the Admin link:**
- Make sure you're logged in with a staff/superuser account
- Check that `user.is_staff = True` or `user.is_superuser = True`

**If you get "Permission Denied":**
- Your account doesn't have staff privileges
- Use Option B above to add staff privileges to your account

