# M-Pesa Integration Setup Guide

This guide will help you set up M-Pesa STK Push integration for the Fundi Platform.

## Prerequisites

1. **M-Pesa Developer Account**: Sign up at https://developer.safaricom.co.ke/
2. **Test Credentials**: Get your test credentials from the developer portal
3. **Production Credentials**: For live payments, you'll need to apply for production credentials

## Step 1: Get M-Pesa Credentials

### For Testing (Sandbox):
1. Go to https://developer.safaricom.co.ke/
2. Sign up/Login to your account
3. Navigate to "My Apps" and create a new app
4. Get the following credentials:
   - **Consumer Key**
   - **Consumer Secret**
   - **Shortcode** (e.g. 600000 — as configured for your sandbox/till)
   - **Passkey** (Get from the app details)

### For Production:
1. Apply for production credentials through the M-Pesa Developer Portal
2. Complete the necessary documentation and approval process
3. Get production credentials once approved

## Step 2: Configure Settings

Update `fundi_platform/settings.py` with your M-Pesa credentials:

```python
# M-Pesa Daraja API Settings
MPESA_CONSUMER_KEY = 'your_consumer_key_here'
MPESA_CONSUMER_SECRET = 'your_consumer_secret_here'
MPESA_SHORTCODE = '600000'  # Your sandbox shortcode (updated from 174379)
MPESA_PASSKEY = 'your_passkey_here'
MPESA_API_URL = 'https://sandbox.safaricom.co.ke'  # For testing
# MPESA_API_URL = 'https://api.safaricom.co.ke'  # For production
MPESA_CALLBACK_URL = 'http://your-domain.com/mpesa/callback/'
```

**Important**: Replace `your-domain.com` with your actual domain name. For local testing, you can use:
- **ngrok** or similar tunneling service to expose your local server
- Example: `https://your-ngrok-url.ngrok.io/mpesa/callback/`

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Run Migrations

After updating the Payment model with new fields:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 5: Test the Integration

### Using Test Credentials:

1. **Test Phone Numbers**: Use M-Pesa test numbers (e.g., 254708374149)
2. **Test PIN**: Use the test PIN provided in the developer portal
3. **Test Amount**: Use small amounts for testing

### Testing Flow:

1. Create a booking as a customer
2. Go to booking details and click "Pay Now"
3. Select "M-Pesa" as payment method
4. Enter a test phone number (format: 254XXXXXXXXX)
5. Click "Complete Payment"
6. You should receive an STK push on your phone
7. Enter the test PIN
8. Payment should be processed and callback received

## Step 6: Production Setup

### Requirements:
1. **HTTPS**: Your callback URL must use HTTPS
2. **Valid Domain**: Use a real domain name (not localhost)
3. **Production Credentials**: Get approved production credentials
4. **SSL Certificate**: Ensure your server has a valid SSL certificate

### Update Settings for Production:

```python
MPESA_API_URL = 'https://api.safaricom.co.ke'  # Production URL
MPESA_SHORTCODE = 'your_production_shortcode'
MPESA_PASSKEY = 'your_production_passkey'
MPESA_CALLBACK_URL = 'https://yourdomain.com/mpesa/callback/'
```

## Troubleshooting

### Common Issues:

1. **"Failed to get access token"**
   - Check your Consumer Key and Consumer Secret
   - Ensure they're correct in settings.py

2. **"STK push not received"**
   - Verify phone number format (must start with 254)
   - Check if using test phone numbers for sandbox
   - Ensure network connectivity

3. **"Callback not received"**
   - Verify callback URL is accessible (use ngrok for local testing)
   - Check server logs for errors
   - Ensure CSRF exemption is working

4. **"Payment status not updating"**
   - Check webhook/callback endpoint is working
   - Verify database migrations ran successfully
   - Check server logs for callback processing errors

### Testing Callback Locally:

**IMPORTANT**: M-Pesa requires a publicly accessible HTTPS URL. Localhost URLs will NOT work!

Use **ngrok** to expose your local server:

1. **Install ngrok**:
   - Download from https://ngrok.com/
   - Or use: `choco install ngrok` (Windows) or `brew install ngrok` (Mac)

2. **Run ngrok**:
   ```bash
   ngrok http 8000
   ```

3. **Copy the HTTPS URL** (looks like: `https://abc123.ngrok.io`)

4. **Update your .env file**:
   ```env
   MPESA_CALLBACK_URL=https://abc123.ngrok.io/mpesa/callback/
   ```
   Replace `abc123.ngrok.io` with your actual ngrok URL

5. **Restart your Django server**:
   ```bash
   python manage.py runserver
   ```

6. **Now try the payment again** - the STK push should work!

**Note**: Each time you restart ngrok, you'll get a new URL. Update your `.env` file accordingly.

## Security Notes

1. **Never commit credentials**: Use environment variables or a `.env` file
2. **Use HTTPS**: Always use HTTPS in production
3. **Validate callbacks**: Verify callback authenticity (implement signature validation)
4. **Log transactions**: Keep logs of all payment transactions
5. **Handle errors**: Implement proper error handling and retry logic

## Environment Variables (Recommended)

For better security, use environment variables:

```python
# In settings.py
import os
from decouple import config

MPESA_CONSUMER_KEY = config('MPESA_CONSUMER_KEY')
MPESA_CONSUMER_SECRET = config('MPESA_CONSUMER_SECRET')
MPESA_SHORTCODE = config('MPESA_SHORTCODE')
MPESA_PASSKEY = config('MPESA_PASSKEY')
MPESA_API_URL = config('MPESA_API_URL', default='https://sandbox.safaricom.co.ke')
MPESA_CALLBACK_URL = config('MPESA_CALLBACK_URL')
```

Create a `.env` file (don't commit it):

```
MPESA_CONSUMER_KEY=your_key_here
MPESA_CONSUMER_SECRET=your_secret_here
MPESA_SHORTCODE=600000
MPESA_PASSKEY=your_passkey_here
MPESA_API_URL=https://sandbox.safaricom.co.ke
MPESA_CALLBACK_URL=https://your-domain.com/mpesa/callback/
```

## API Documentation

For more details, refer to:
- M-Pesa Daraja API Documentation: https://developer.safaricom.co.ke/APIs
- STK Push API: https://developer.safaricom.co.ke/APIs/MpesaExpressSimulate

## Support

For M-Pesa API issues:
- M-Pesa Developer Portal: https://developer.safaricom.co.ke/
- Support: developer@safaricom.co.ke

